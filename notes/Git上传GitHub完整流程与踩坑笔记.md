# Git 上传 GitHub 完整流程与踩坑笔记

> 学习记录:第一次将本地代码上传 GitHub 的完整过程,包含遇到的全部问题及解决方案。
> 环境:Windows + PowerShell + PyCharm + Git 2.54.0

---

## 一、核心概念(先理解再操作)

| 概念 | 人话解释 |
|------|----------|
| Git | 装在自己电脑上的版本管理工具,负责记录代码的每次变化 |
| GitHub | 云端的代码仓库网站,用来存放和展示代码 |
| 仓库(repository) | 一个项目的"文件夹",本地一个,GitHub 上一个,互为镜像 |
| add | 把改动的文件"装进箱子"(暂存) |
| commit | "封箱贴标签",在本地记录一次提交,标签就是提交说明 |
| push | "把箱子寄出去",将本地提交上传到 GitHub |
| pull | 反向操作,把 GitHub 上的内容拉到本地 |
| .gitignore | 一份清单,告诉 Git 哪些文件永远不要管(如 IDE 配置) |

**重要原则:本地是源头,GitHub 只是镜像。** 所有删改都从本地走命令再 push,不要在 GitHub 网页上直接改,否则两边会产生分叉。

---

## 二、一次性配置(只做一次,以后不用重复)

### 1. 安装 Git

- 下载地址:https://git-scm.com
- 安装时一路默认选项即可
- 验证安装:终端输入 `git --version`,能显示版本号即成功

### 2. 配置身份(提交记录上的署名)

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

> 注:这里的 name 不需要和 GitHub 用户名一致,只是署名,不影响连接。

### 3. 在 GitHub 上建仓库

1. 登录 github.com → 右上角 `+` → New repository
2. 取仓库名(如 `daily-practice`)
3. 选 **Public**(公开,面试官才能看到)
4. 勾选 "Add a README file"
5. 点 Create

### 4. 本地文件夹与 GitHub 仓库关联

在项目文件夹的终端里执行:

```bash
git init                      # 把当前文件夹变成 Git 仓库
git remote add origin https://github.com/用户名/仓库名.git   # 绑定远程地址
git pull origin main          # 把 GitHub 上的 README 拉下来
```

> 注意:remote 地址里的用户名和仓库名必须与网页地址栏完全一致(大小写、横杠)。
> 查看自己的用户名:GitHub 网页右上角头像 → 弹出菜单第一行。
> 如果地址写错了,用 `git remote set-url origin 新地址` 修改。

### 5. 第一次 push 的登录授权

第一次 `git push` 会弹出登录窗口:

- 选 **Sign in with your browser**(用浏览器登录)
- 浏览器里点 Authorize 授权
- 凭证会保存在电脑里,以后不再需要登录

---

## 三、每日固定操作(以后只用记这三行)

```bash
git add .                          # 装箱:把今天的改动全部暂存
git commit -m "第X天:今天做了什么"   # 封箱贴标签
git push origin main               # 寄出:上传到 GitHub
```

**好习惯:**

- commit 说明认真写("第5天:泰坦尼克分组统计获救率" 远好于 "update"),这是给面试官看的学习轨迹
- commit 之前先 `git status` 检查要提交的内容,像寄快递前看一眼箱子里装的是什么
- 按键盘 ↑ 可以调出上一条命令,不用重复打字

---

## 四、踩坑实录与解决方案

### 坑1:push/pull 报错 "Failed to connect to github.com port 443"

**症状:**

```
fatal: unable to access 'https://...': Failed to connect to github.com port 443 ... Could not connect to server
```

**原因:** 网络到不了 GitHub 服务器(国内常见)。注意:这不是命令错误,也不是用户名错误——如果是用户名/仓库名写错,报错会是 "repository not found"。

**排查顺序:**

1. `ping github.com` + 浏览器试开 github.com,判断网络状况
2. **浏览器能开但终端连不上** → 电脑上开着代理软件,但终端没走代理。给 Git 配置代理(端口号看代理软件设置,常见 7890):

   ```bash
   git config --global http.proxy http://127.0.0.1:7890
   git config --global https.proxy http://127.0.0.1:7890
   ```

   取消代理(以后不用时):

   ```bash
   git config --global --unset http.proxy
   git config --global --unset https.proxy
   ```

3. **浏览器也打不开** → 单纯网络问题,等待重试、或切手机热点(流量访问 GitHub 通常更稳)
4. 失败就按 ↑ 重试,网络抽风时多试几次经常就通了

**本次实际解决:** 配置了 `127.0.0.1:7897` 代理后立刻成功。

**经验:** 开机后先确认代理软件在运行,再 push。

---

### 坑2:.idea 文件夹被传上了 GitHub

**症状:** GitHub 仓库里出现 `.idea/` 文件夹(misc.xml、modules.xml 等)。

**原因:** `.idea` 是 PyCharm 的工程配置,不是代码,`git add .` 把它一起装箱了。传上去显得不专业,还可能泄露本机路径信息。

**解决:** 建 `.gitignore` 文件,内容写一行:

```
.idea/
```

然后把已被追踪的 .idea 移除:

```bash
git rm -r --cached .idea    # 只从 Git 追踪中移除,本地文件不动
git add .
git status                  # 检查:应全是 deleted: .idea/...
git commit -m "移除IDE配置文件"
git push origin main
```

**经验:** 以后每个新项目第一件事就是建 `.gitignore`,这是专业习惯。

---

### 坑3:用 echo 创建的 .gitignore 不生效(编码问题)

**症状:**

- `.gitignore` 写了 `.idea/`,但 `git add .` 还是把 .idea 加进来
- GitHub 网页上看 `.gitignore` 内容显示乱码:`��.idea/^M`
- `git check-ignore -v .idea` 没有任何输出

**原因:** PowerShell 的 `echo xxx > 文件` 默认用 **UTF-16 编码** 写文件,而 Git 只认 UTF-8。用 `Format-Hex .gitignore` 查看字节,开头出现 `FF FE` 即为 UTF-16 的标志。

**关键教训:** `cat` 显示正常 ≠ 文件真的正常(PowerShell 会"美化"显示),**Hex 字节才是终极真相**。遇到"文件内容明明对但程序读不了",第一反应查编码。

**解决(任选其一):**

- 用 PyCharm 直接编辑保存(IDE 默认 UTF-8)
- 用 Python 写文件(最可靠):

  ```bash
  python -c "open('.gitignore','w',encoding='utf-8').write('.idea/\n')"
  ```

**验证修复:** `Format-Hex .gitignore` 应显示 `2E 69 64 65 61 2F`(纯 UTF-8 的 `.idea/`),开头无 `FF FE`。

---

### 坑4:git rm --cached 之后又被 git add . 加回去

**症状:** 执行了 `git rm -r --cached .idea`,接着 `git add .`,结果 commit 时提示 "nothing to commit"——一出一进抵消了。

**原因:** 此时 `.gitignore` 还没生效(坑3的编码问题),Git 不知道要忽略 .idea,`add .` 又把它装回箱子。

**正确顺序:** 先确保 `.gitignore` 生效,再执行移除。每一步用 `git status` 确认。

---

### 坑5:check-ignore 没输出 ≠ 规则没生效

**症状:** `.gitignore` 编码已修好,但 `git check-ignore -v .idea` 依然没有输出。

**原因:** Git 特性——**ignore 规则只对"未被追踪"的文件生效**。.idea 之前被提交过、还在追踪名单里,所以 check-ignore 默认不报告它。

**正确验证方式:**

```bash
git check-ignore --no-index -v .idea    # --no-index = 不管追踪状态,纯测规则
```

**理解:** 对已追踪的文件,必须先 `git rm -r --cached` 解除追踪,ignore 规则才会接管。

---

## 五、常用命令速查

```bash
# 查看
git status                    # 当前状态(必备,commit 前先看)
git log --oneline             # 提交历史
cat .gitignore                # 查看文件内容(注意:显示正常不代表编码正常)
Format-Hex 文件名              # 查看文件真实字节(PowerShell)

# 配置
git config --global user.name "名字"
git config --global user.email "邮箱"
git remote set-url origin 新地址      # 修改远程仓库地址
git config --global http.proxy http://127.0.0.1:端口    # 设置代理
git config --global --unset http.proxy                  # 取消代理

# 日常三件套
git add .
git commit -m "说明"
git push origin main

# 排错
git check-ignore --no-index -v 路径   # 测试 ignore 规则是否匹配
git rm -r --cached 路径               # 解除追踪(本地文件保留)
ping github.com                       # 测试网络连通性
```

---

## 六、本次经历的核心收获

1. **报错信息会说话:** "Could not connect" 是网络问题,"repository not found" 才是地址问题。先读懂报错再动手。
2. **每步验证,不要盲跑:** commit 前 `git status`,改完文件后用工具验证,不凭感觉判断"应该好了"。
3. **编码是 Windows 开发的经典坑:** UTF-8 / UTF-16 / BOM,Hex 字节是终极真相。
4. **排查思路比答案重要:** 定位问题(网络?配置?编码?)→ 缩小范围 → 验证假设 → 修复确认。这套流程就是真实的开发日常。

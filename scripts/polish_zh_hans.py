#!/usr/bin/env python3
"""Human-curated Simplified Chinese copy edits for the Pincer UI.

Keeps product names, Swift format arguments and structure intact. Call this
after the optional first-pass translation, not before. All content is public.
"""
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "Sources/PincerUI/Resources/Localizable.xcstrings"
FMT = re.compile(r"%(?:[0-9]+\$)?(?:lld|llu|ld|lu|zd|zu|lf|@|d|i|u|s|f|g|G|e|E|x|X|o|p|c)|%#@[^@]+@|%%")

# Terms and action copy revised for idiomatic, concise iOS Simplified Chinese.
# Exact source keys avoid modifying code snippets, model outputs, and protocol names.
FIXES = {
    "Enter your Gateway's address.": "请输入网关地址。",
    "That doesn't look like a Gateway address. Try something like wss://my-mac.tailnet.ts.net or ws://192.168.1.20:18789.": "地址格式不正确。可以填写 wss://my-mac.tailnet.ts.net 或 ws://192.168.1.20:18789。",
    "For safety, Pincer only uses unencrypted ws:// on this Mac, your local network, or Tailscale. Use a wss:// address instead.": "为保护数据安全，未加密的 ws:// 仅允许用于本机、局域网或 Tailscale。其他网络请使用 wss://。",
    "Can't reach a Gateway at that address. Make sure OpenClaw is running (openclaw gateway status) and that this device can reach it.": "无法连接网关。请确认 OpenClaw 正在运行（openclaw gateway status），并检查手机与网关之间的网络。",
    "Is Tailscale connected on this device?": "请检查这台设备是否已连接 Tailscale。",
    "Something answered, but it isn't an OpenClaw Gateway. Check the address and port (usually 18789).": "这个地址能访问，但它不是 OpenClaw 网关。请检查地址和端口（默认 18789）。",
    "Couldn't make a secure connection to that address. If you use Tailscale Serve, check that HTTPS is enabled for your tailnet.": "无法建立安全连接。如果网关使用自签名证书，请在「高级设置」填写 TLS 证书 SHA-256 指纹；如果使用 Tailscale Serve，请确认 HTTPS 已启用。",
    "The Gateway's certificate doesn't match the fingerprint you entered.": "网关证书与填写的 SHA-256 指纹不匹配。请核对证书或重新获取指纹。",
    "That token didn't work. Copy it again with the command below and paste the whole thing.": "网关令牌无效。请使用下面的命令重新复制完整令牌。",
    "This Gateway needs a token.": "这个网关需要令牌才能登录。",
    "That password didn't work. Check it and try again.": "密码不正确，请检查后重试。",
    "This Gateway uses a password. Choose Use a password instead.": "这个网关使用密码验证。请选择「改用密码登录」。",
    "This Gateway isn't set up for that sign-in method. Try the other one.": "网关没有启用当前验证方式，请尝试另一种方式。",
    "Too many tries. Wait a minute, then try again.": "尝试次数过多，请稍等一分钟再试。",
    "This Gateway's version doesn't work with this Pincer. Update OpenClaw or Pincer.": "当前 OpenClaw 版本与 Pincer 不兼容。请更新其中一个应用。",
    "The Gateway turned down this device. Go back and try again, or approve it with the command above.": "OpenClaw 拒绝了这台设备。请返回重试，或在运行 OpenClaw 的电脑上执行上方命令批准它。",
    "The request changed. Use this new command.": "授权请求已更新，请使用新的命令。",
    "No Gateway needed. Explore sample agents and chats. Nothing leaves this device.": "无需连接 OpenClaw，也可以先体验示例智能体和聊天；演示数据仅保存在本机。",
    "Your Gateway reported a problem. You can keep going and check it later.": "OpenClaw 检测到异常。你可以先继续，稍后再查看详情。",
    "Already use Pincer on another device with Full Management? You can approve this one there, in Gateway Settings → Devices.": "如果你在其他设备上的 Pincer 已获得完整管理权限，也可以前往「网关设置 → 设备」批准这台手机。",
    "Tailscale": "Tailscale",
    "Hide subagent runs": "收起子智能体任务",
    "List subagent runs under their chat": "在会话下显示子智能体任务",
    "No messages to rewind to": "没有可以回溯的消息",
    "Open Chat": "打开会话",
    "Choose a chat": "选择会话",
    "Choose a chat (⌘J or Tab)": "选择会话（⌘J 或 Tab）",
    "Use Find in Chat to search the current chat.": "使用「搜索当前会话」查找消息。",
    "Message search needs the transcript cache, which is turned off.": "消息搜索需要聊天记录缓存，请先在设置中开启缓存。",
    "Quick Capture, unread chats, approvals and Gateway status, one click away.": "快速记录、未读消息、操作审批和网关状态，一点即达。",
    "No bindings. Messages reach this agent only when it's the default or chosen directly.": "还没有消息路由规则。只有设为默认智能体或手动选择时，消息才会发给它。",
    "No messages to rewind to": "没有可以回溯的消息",
    "Session Usage…": "会话用量…",
    "Session ID": "会话 ID",
    "Open Chat in New Window": "在新窗口中打开会话",
    "Search Messages…": "搜索消息…",
    "Search messages in every chat on %@.": "搜索 %@ 中的全部会话。",
    "Search messages for “%@”": "搜索包含「%@」的消息",
    "Pincer starts a chat called %@ with %@.": "Pincer 将与 %2$@ 创建一个名为「%1$@」的会话。",
    "Each run starts a fresh chat under Automations in the sidebar.": "每次运行自动化任务都会在侧边栏「自动化任务」下新建会话。",
    "Pick your default agent and model, look over skills, then send a test message. Skip anything you like.": "选择默认智能体和模型，按需检查技能，再发一条消息测试。暂时不想设置的步骤可以跳过。",
    "Save Model": "保存模型设置",
    "No models available": "没有可用的模型",
    "Reconnecting in %llds (attempt %lld)": "%1$lld 秒后重连（第 %2$lld 次尝试）",
    "Queue Message": "稍后发送",
    "No chat selected": "还没有选择会话",
    "No Gateways yet": "尚未连接 OpenClaw",
    "Same Wi-Fi": "同一 Wi-Fi",
    "Step %lld of %lld · %@": "第 %1$lld/%2$lld 步 · %3$@",
    "Find": "查找网关",
    "Get started": "开始使用",
    "Sign in": "登录",
    "Verify": "验证连接",
    "Set up": "初始设置",
    "Done": "完成",
    "Find your Gateway": "查找 OpenClaw 网关",
    "Where is OpenClaw running?": "OpenClaw 运行在哪台设备上？",
    "Your Gateway is on this network and set to accept connections from it.": "OpenClaw 与手机位于同一局域网，并已允许局域网设备连接。",
    "Your Gateway is on another device in your tailnet. Turn on Tailscale Serve on the Gateway host, then use its address.": "如果 OpenClaw 在其他设备上，请先在那台设备启用 Tailscale Serve，再填入对应地址。",
    "OpenClaw is running on this Mac.": "OpenClaw 运行在这台 Mac 上。",
    "This Mac": "这台 Mac",
    "Gateway address": "网关地址",
    "Gateway URL": "网关地址",
    "Advanced…": "高级设置…",
    "Help me choose": "如何选择？",
    "Continue Anyway": "仍要继续",
    "Try Again": "重试",
    "Try the Demo": "体验演示",
    "Welcome to Pincer": "欢迎使用 Pincer",
    "Do you have an OpenClaw Gateway?": "你已经运行 OpenClaw 了吗？",
    "No Gateway yet? Explore Pincer with sample agents and chats. Nothing leaves this device.": "还没安装 OpenClaw？先体验一下示例聊天和智能体。演示数据只保存在本机。",
    "Pincer connects to a Gateway you run on your own computer or server.": "Pincer 可以连接你在电脑或服务器上运行的 OpenClaw。",
    "My Gateway Is Running": "已经运行 OpenClaw",
    "Install OpenClaw": "安装 OpenClaw",
    "Get Started": "开始使用",
    "Pincer will connect to %@": "将连接到 %@",
    "Checking…": "正在检查连接…",
    "Couldn’t connect": "连接失败",
    "Couldn't connect": "连接失败",
    "Connection timeout": "连接超时",
    "Can't reach Gateway · retrying in %llds": "无法连接网关，%lld 秒后重试",
    "Connected": "已连接",
    "Not Connected": "未连接",
    "Not connected": "未连接",
    "Connecting…": "正在连接…",
    "Connected to %@": "已连接到 %@",
    "Connecting to %@…": "正在连接 %@…",
    "You're connected": "连接成功",
    "Sign in to your Gateway": "验证网关身份",
    "Paste your Gateway token. You'll only need to do this once.": "粘贴 OpenClaw 的网关令牌，只需设置一次。",
    "Sign-in didn't finish.": "身份验证未完成。",
    "Signing in…": "正在验证身份…",
    "Sign In": "登录",
    "Sign In Again": "重新登录",
    "Gateway token": "网关令牌",
    "Gateway password": "网关密码",
    "For your security, new devices must be approved on the machine running OpenClaw. Run this there:": "为了安全，需要在运行 OpenClaw 的电脑上批准这台设备。请在那台电脑执行：",
    "For your security, new devices need your OK. Run this on the Gateway host:": "为保护你的数据，请先在运行 OpenClaw 的电脑上执行以下命令，批准这台设备：",
    "Approve Pincer on your Gateway": "在 OpenClaw 中批准 Pincer",
    "Approve Pincer on your Gateway host": "在运行 OpenClaw 的电脑上批准 Pincer",
    "Approve this device on the Gateway host:": "请在运行 OpenClaw 的电脑上批准这台设备：",
    "Find Pincer in the list and approve its request ID.": "在设备列表中找到 Pincer，批准对应的请求 ID。",
    "Waiting for approval…": "等待设备授权…",
    "Waiting for approval": "等待设备授权",
    "Waiting for approval on the Gateway host": "等待 OpenClaw 批准这台设备",
    "If you changed settings, the request ID may have changed. Run openclaw devices list to see the latest one.": "如果你刚修改过设置，请求 ID 可能已经变化。运行 openclaw devices list 查看最新请求。",
    "Tailscale Serve uses HTTPS, so this should usually be wss://. Use ws:// only with the tailnet IP and Gateway port.": "使用 Tailscale Serve 时通常填 wss:// 地址。只有直接连接 Tailscale IP 和网关端口时才用 ws://。",
    "Use your Tailscale Serve name (wss://…ts.net) or tailnet IP (ws://100.x.y.z:18789). Plain ws:// is only allowed for Tailscale, LAN and loopback addresses.": "可填 Tailscale Serve 域名（wss://…ts.net），或 Tailscale IP（ws://100.x.y.z:18789）。未加密的 ws:// 仅限局域网、Tailscale 网络和本机使用。",
    "Full Management": "完整管理权限",
    "Full Management Needed": "需要完整管理权限",
    "Needs Full Management": "需要完整管理权限",
    "Needs Full Management access": "需要完整管理权限",
    "Open Connection": "打开连接设置",
    "Open Connection…": "打开连接设置…",
    "Open Connection to turn on Full Management.": "在连接设置中开启完整管理权限。",
    "The Gateway hasn't granted Full Management to this device yet.": "OpenClaw 尚未向这台设备授予完整管理权限。",
    "Full Management lets Pincer change Gateway settings and agents. You can turn it on later in Connection.": "开启完整管理权限后，Pincer 才能修改网关设置和智能体。也可以稍后在连接设置中开启。",
    "Changing Gateway settings needs Full Management access. Turn it on under Connection, then approve this device on the Gateway host.": "要修改网关设置，请先在「连接」中开启完整管理权限，并在 OpenClaw 所在设备上批准授权。",
    "Changing automations needs Full Management access. Turn it on under Gateway Settings → Connection, then approve this device on the Gateway host.": "要修改自动化任务，请前往「网关设置 → 连接」开启完整管理权限，并在 OpenClaw 所在设备上批准。",
    "Changing the Gateway voice needs Full Management access. Ask the Gateway owner to approve it for this device.": "要修改网关语音设置，需要完整管理权限。请让网关所有者为这台设备授权。",
    "Editing agents needs Full Management": "编辑智能体需要完整管理权限",
    "Editing agents needs Full Management. Turn it on under Connection, then approve this device on the Gateway host.": "要编辑智能体，请先在「连接」中开启完整管理权限，并在运行 OpenClaw 的设备上批准授权。",
    "Approving, rejecting and revoking devices needs Full Management. Turn it on under Connection.": "批准、拒绝或撤销设备授权需要完整管理权限。请先在「连接」中开启。",
    "Turn on Full Management under Connection, then approve this device on the Gateway host.": "请在「连接」中开启完整管理权限，再到运行 OpenClaw 的设备上批准授权。",
    "You can view agents and their files. Turn on Full Management under Connection, then approve this device on the Gateway host.": "目前只能查看智能体及其文件。要修改内容，请在「连接」中开启完整管理权限，并在 OpenClaw 所在设备上批准。",
    "You can view skills. Turn on Full Management under Connection, then approve this device on the Gateway host.": "目前只能查看技能。要管理技能，请在「连接」中开启完整管理权限，并在 OpenClaw 所在设备上批准。",
    "You can read this file. Turn on Full Management under Connection, then approve this device on the Gateway host.": "目前只能查看该文件。要编辑，请在「连接」中开启完整管理权限，并在 OpenClaw 所在设备上批准。",
    "The Gateway config has model \"%@\", which is ignored. Choose a model here to replace it.": "网关配置中的模型「%@」未生效。请在这里重新选择模型。",
    "Each agent has its own identity, model and workspace.": "每个智能体都有独立的身份、模型和工作区。",
    "Chat with your OpenClaw agents from your Mac, iPhone, and iPad.": "在 Mac、iPhone 和 iPad 上与 OpenClaw 智能体聊天。",
    "Chat": "聊天",
    "Chats": "聊天",
    "Message": "消息",
    "Messages": "消息",
    "Main chat": "主会话",
    "Choose a chat from the sidebar or start a new one.": "从侧边栏选择一个会话，或开始新聊天。",
    "New Chat": "新建聊天",
    "New chat": "新建聊天",
    "Go to Chats": "进入聊天",
    "No chat selected": "尚未选择会话",
    "No messages match “%@”.": "没有找到包含「%@」的消息。",
    "Scroll to latest message": "回到最新消息",
    "Loading messages": "正在加载消息",
    "Loading earlier messages": "正在加载历史消息",
    "Copy message": "复制消息",
    "Copy Reply": "复制回复",
    "Regenerate Last Reply": "重新生成上条回复",
    "Edit Last Message": "编辑上一条消息",
    "Cancel reply": "取消回复",
    "Typing": "正在输入",
    "Thinking": "思考中",
    "Show Thinking Steps": "展开思考过程",
    "Hide Thinking Steps": "收起思考过程",
    "Include Thinking": "包含思考过程",
    "Include thinking": "包含思考过程",
    "Include tool calls": "包含工具调用",
    "Ask for deeper reasoning with /think. Expand a thinking section to read it.": "输入 /think 可以请求更深入的思考。点击思考卡片即可展开查看。",
    "Earlier messages were summarized for the agent. They're still shown here.": "较早的消息已摘要压缩，供智能体继续理解上下文；原始消息仍可在这里查看。",
    "Filling up. Compacting summarizes older messages to free room.": "上下文快满了。压缩后会用摘要替代较早的消息，腾出空间。",
    "Offline — messages send when you reconnect": "当前离线，重连后会自动发送",
    "Queue Message": "加入待发送队列",
    "No models available": "暂无可用模型",
    "Choose a model…": "选择模型…",
    "Model ID": "模型 ID",
    "Open Agents & Models": "打开「智能体与模型」",
    "Open Gateway Health": "查看网关运行状况",
    "Gateway Logs needs the operator.read scope. Approve it for this device on the Gateway host, then try again.": "查看网关日志需要 operator.read 权限。请在运行 OpenClaw 的设备上为这台手机授权后重试。",
    "Approval History needs the operator.approvals scope. Approve it for this device on the Gateway host, then try again.": "查看审批记录需要 operator.approvals 权限。请在运行 OpenClaw 的设备上授权后重试。",
    "Approval History": "审批记录",
    "Approval History…": "审批记录…",
    "Approval History Isn't Available": "暂时无法查看审批记录",
    "No Approval History": "暂无审批记录",
    "approval history": "审批记录",
    "approval pending": "等待审批",
    "approval unavailable": "审批不可用",
    "Waiting for approval": "等待审批",
    "Approve": "允许",
    "Approved": "已允许",
    "Deny": "拒绝",
    "Denied": "已拒绝",
    "Allow Once": "仅允许这次",
    "Always Allow": "始终允许",
    "No allowed commands. When you choose **Always allow** on an approval, the command is added here.": "还没有始终允许的命令。审批时选择「始终允许」，相应命令会出现在这里。",
    "No allowed tools. When you choose **Always allow** on a tool approval, the tool is added here.": "还没有始终允许的工具。审批时选择「始终允许」，相应工具会出现在这里。",
    "Decisions on commands, plugins and system changes show up here for 30 days. Pending approvals appear in the chat.": "这里会保留最近 30 天的命令、插件和系统操作审批记录。待审批的操作会直接显示在聊天中。",
    "Quick Capture": "快速记录",
    "Quick Capture, unread chats, approvals and Gateway status, one click away.": "快速记录、未读消息、操作审批和网关状态，一点即达。",
    "Add a Gateway in Pincer to use Quick Capture": "先在 Pincer 中连接 OpenClaw，才能使用「快速记录」。",
    "Open a small composer from any app to send to a chat.": "从任意 App 唤出快捷输入框，直接把内容发送到聊天。",
    "Start Pincer when you log in, so Quick Capture is ready.": "登录 Mac 后自动启动 Pincer，随时使用「快速记录」。",
    "Device name": "设备名称",
    "Devices": "设备",
    "Paired Devices": "已配对设备",
    "This device was already revoked.": "这台设备的授权已被撤销。",
    "This node was already removed.": "这个节点已经移除。",
    "Gateway logs are redacted by the Gateway, but they can still contain hostnames, file paths and message content. Review them before sharing.": "虽然网关会隐藏部分敏感信息，日志仍可能包含主机名、文件路径和消息内容。分享前请仔细检查。",
    "The Gateway downloads and installs the plugin itself. Only install plugins you trust: they run on your Gateway host.": "插件由 OpenClaw 自行下载并安装。插件会在你的电脑或服务器上运行，只安装你信任的插件。",
    "Plugins run on your Gateway host. Turning one on or off, installing or removing it happens right away.": "插件运行在 OpenClaw 所在的设备上。启用、停用、安装和卸载操作会立即生效。",
    "Installers": "安装器",
    "Installers run on the Gateway host to add what the skill needs.": "安装器会在 OpenClaw 所在设备上运行，为技能准备依赖环境。",
    "The folder on the Gateway host with this agent's files.": "OpenClaw 所在设备上存放该智能体文件的目录。",
    "Add skills to the agent's workspace on the Gateway host.": "为 OpenClaw 所在设备上的智能体工作区添加技能。",
    "Branch from Here": "从这里创建分支",
    "Branches need a newer Gateway.": "此功能需要更新版本的 OpenClaw。",
    "Switching branches needs Full Management access.": "切换会话分支需要完整管理权限。",
    "Gateway logs are redacted by the Gateway, but they can still contain hostnames, file paths and message content. Review them before sharing": "网关日志可能包含主机名、文件路径或消息内容。分享前请仔细检查。",
    "It stops running and its run history is removed from the Gateway. Its chats stay.": "任务将停止运行，执行历史也会从网关删除；聊天记录会保留。",
    "The Gateway waits for running replies and tasks to finish, then restarts. Pincer reconnects on its own.": "OpenClaw 会等待当前回复和任务结束后重启，Pincer 随后自动重连。",
    "Chats are downloaded again from your Gateways when you open them, and message search is rebuilt. Nothing on your Gateways is deleted.": "打开聊天后会重新从网关获取记录，并重建搜索索引。网关上的聊天记录不会被删除。",
    "Chat titles appear in Spotlight. Message text comes from the last few cached messages and never leaves this device.": "聊天标题会显示在 Spotlight 搜索中。消息预览只来自本机缓存，不会被上传。",
    "Messages you send here go straight to your Gateway as the owner.": "这里发送的消息会以网关所有者的身份直接发给 OpenClaw。",
    "Queued and failed messages, and their attachments, are deleted from this device without being sent. Chats and cached transcripts aren’t affected.": "会从此设备删除待发送和发送失败的消息及附件，不会将它们发送出去；现有聊天和缓存不受影响。",
    "Which commands your agents can run on the Gateway host, and when they have to ask.": "控制智能体可以在 OpenClaw 所在设备上执行哪些命令，以及哪些操作必须先征得你的同意。",
    "View details": "查看详情",
    "No Gateways yet": "尚未连接 OpenClaw",
    "No Gateway yet? Explore Pincer with sample agents and chats. Nothing leaves this device.": "还没安装 OpenClaw？先体验示例聊天和智能体。演示数据只保存在本机。",
    "Search chats and agents": "搜索会话和智能体",
    "Search chats and agents…": "搜索会话和智能体…",
    "Jump to a chat or run a command…": "跳转到会话或运行命令…",
    "Find in Chat": "搜索当前会话",
    "Find in Chat…": "搜索当前会话…",
    "Find a chat": "查找会话",
    "Finish opens this chat.": "完成后打开这个会话。",
    "Done": "完成",
    "Cancel": "取消",
    "Try Again": "重试",
}
EXTRA_UI = {
    "Find": "查找网关",
    "Sign in": "登录",
    "Set up": "配置",
    "Verify": "验证",
    "Get started": "开始使用",
}
FIRST_RUN_ERRORS = {
    "Enter your Gateway's address.",
    "That doesn't look like a Gateway address. Try something like wss://my-mac.tailnet.ts.net or ws://192.168.1.20:18789.",
    "For safety, Pincer only uses unencrypted ws:// on this Mac, your local network, or Tailscale. Use a wss:// address instead.",
    "Can't reach a Gateway at that address. Make sure OpenClaw is running (openclaw gateway status) and that this device can reach it.",
    "Is Tailscale connected on this device?",
    "Something answered, but it isn't an OpenClaw Gateway. Check the address and port (usually 18789).",
    "Couldn't make a secure connection to that address. If you use Tailscale Serve, check that HTTPS is enabled for your tailnet.",
    "The Gateway's certificate doesn't match the fingerprint you entered.",
    "That token didn't work. Copy it again with the command below and paste the whole thing.",
    "This Gateway needs a token.",
    "That password didn't work. Check it and try again.",
    "This Gateway uses a password. Choose Use a password instead.",
    "This Gateway isn't set up for that sign-in method. Try the other one.",
    "Too many tries. Wait a minute, then try again.",
    "This Gateway's version doesn't work with this Pincer. Update OpenClaw or Pincer.",
    "The Gateway turned down this device. Go back and try again, or approve it with the command above.",
    "The request changed. Use this new command.",
    "No Gateway needed. Explore sample agents and chats. Nothing leaves this device.",
    "Your Gateway reported a problem. You can keep going and check it later.",
    "Already use Pincer on another device with Full Management? You can approve this one there, in Gateway Settings → Devices.",
}
CHINESE = re.compile(r"[\u3400-\u9fff]")

def units(v):
    if isinstance(v,dict):
        if isinstance(v.get("stringUnit"),dict) and "value" in v["stringUnit"]:
            yield v["stringUnit"]
        for k,x in v.items():
            if k!="stringUnit":yield from units(x)
    elif isinstance(v,list):
        for x in v:yield from units(x)

def polish(en, zh):
    if en in FIXES:
        return FIXES[en]
    if "您的" in zh or "您" in zh:
        zh=zh.replace("您的","你的").replace("您","你")
    en_low=en.lower()
    if "tailscale" in en_low or "tailnet" in en_low:
        zh=zh.replace("尾鳞","Tailscale").replace("尾网","Tailscale 网络")
    if "pincer" in en_low:
        zh=zh.replace("钳子","Pincer").replace("夹子","Pincer")
    if re.search(r"\bagents?\b",en_low) and "proxy" not in en_low:
        zh=zh.replace("代理","智能体").replace("客服人员","智能体")
    if "full management" in en_low:
        zh=zh.replace("完全管理访问权限","完整管理权限").replace("全面管理访问权限","完整管理权限").replace("全面管理","完整管理权限").replace("完全管理","完整管理权限")
        zh=zh.replace("完整管理权限权限","完整管理权限")
    if "gateway host" in en_low:
        zh=zh.replace("网关主机","运行 OpenClaw 的设备").replace("网关服务器","OpenClaw 所在设备")
    if "quick capture" in en_low:
        zh=zh.replace("快速捕获","快速记录")
    if re.search(r"\bmodels?\b",en_low):
        zh=zh.replace("型号","模型").replace("模特","模型")
    if "branch" in en_low and "branch office" not in en_low:
        zh=zh.replace("分支机构","分支")
    if "composer" in en_low:
        zh=zh.replace("作曲器","输入框").replace("作曲家","输入框")
    if "transcript" in en_low:
        zh=zh.replace("转录本","聊天记录")
    if "spotlight" in en_low:
        zh=zh.replace("聚光灯","Spotlight")
    if re.search(r"\binstaller\b",en_low):
        zh=zh.replace("安装人员","安装器")
    if "device" in en_low:
        zh=zh.replace("装置","设备")
    if "subagent" in en_low:
        zh=zh.replace("子代理","子智能体")
    if re.search(r"\bchannels?\b",en_low):
        zh=zh.replace("通道","频道").replace("渠道","频道")
    if re.search(r"\baccounts?\b",en_low):
        zh=zh.replace("帐户","账号")

    # Unwanted and inconsistent Chinese punctuation introduced by MT
    if en.endswith("…") and zh.endswith("..."):
        zh=zh[:-3]+"…"
    return zh

def main():
    cat=json.loads(CAT.read_text(encoding="utf-8"))
    for en,cn in {**EXTRA_UI, **{k:v for k,v in FIXES.items() if k in FIRST_RUN_ERRORS}}.items():
        if en not in cat["strings"]:
            cat["strings"][en]={
                "localizations":{
                    "en":{"stringUnit":{"state":"translated","value":en}},
                    "zh-Hans":{"stringUnit":{"state":"translated","value":cn}},
                }
            }
    edited=[]
    mismatched=[]
    for key,entry in cat["strings"].items():
        enu=list(units(entry["localizations"]["en"]))
        zhu=list(units(entry["localizations"]["zh-Hans"]))
        for a,b in zip(enu,zhu):
            old=b["value"]
            new=polish(key,old)
            if collections.Counter(FMT.findall(a["value"])) != collections.Counter(FMT.findall(new)):
                mismatched.append((key,a["value"],new))
                continue
            if old!=new:
                b["value"]=new
                edited.append((key,old,new))
    if mismatched:
        for m in mismatched[:10]:print("PLACEHOLDER MISMATCH",m)
        raise SystemExit(f"Failed: {len(mismatched)} unsafe placeholders")
    CAT.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Polished {len(edited)} UI string units; catalog entries={len(cat['strings'])}")
    for k,old,new in edited[:14]:print(f"  {k[:65]}: {old[:38]} => {new[:50]}")
if __name__=="__main__":
    main()

# Pincer 简体中文 iPhone 版

这是 Pincer 官方源码的汉化分支，保留原生 SwiftUI 界面和 Gateway WebSocket 通信。
原版许可证 MIT，不改动 OpenClaw Gateway，不公开 Gateway 凭据。

## 云端编译

打开本仓库 Actions → Pincer 简体中文版 iOS IPA → Run workflow（推送 zh-hans-ios 分支也会自动触发）。
完成后在 Artifacts 下载 Pincer-zh-Hans-unsigned-IPA，解压得到 Pincer-zh-Hans-unsigned.ipa。

此 IPA **未签名**，不能直接在 iPhone 点击安装；可以使用 Sideloadly 或 SideStore 通过自己的 Apple ID 重签名。免费账户通常每 7 天续签。
可能需要在侧载工具内更改 Bundle ID 并清除部分不支持的 entitlements。IPA 打包时省略了分享和通知扩展，分享与部分推送可能不可用。本项目未完成实体 iPhone 安装验证。

安装后正常连接并批准你自己运行的 OpenClaw Gateway 设备；远程优先使用家庭 VPN，不要把 Gateway 裸露公网，不要上传任何 Gateway token、密码、聊天或苹果账号数据。

## 翻译与校验

Sources/PincerUI/Resources/Localizable.xcstrings 增加 zh-Hans 目录。常用界面术语采用固定词表，其余仅对官方公开英文 UI 文案进行可选在线翻译（Google 非官方网页接口，可能限流），中文结果与缓存一并提交，GitHub Actions 不调用翻译服务。
运行 python3 scripts/translate_zh_hans.py --check 可查看真实中文覆盖、英语残留数及动态占位符安全校验。机器翻译需要实际人工校对。部分未进入 Apple 字符串目录的硬编码文案仍可能显示英文。

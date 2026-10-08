#!/usr/bin/env python3
"""Add reproducible zh-Hans localization to Pincer (public UI strings only).

Usage:
  python3 scripts/translate_zh_hans.py --max-batches 200
  python3 scripts/translate_zh_hans.py --check

Google's public website endpoint is optional and unofficial; translations are
cached in git, so building an IPA never needs internet access.
"""
import argparse
import collections
from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "Sources/PincerUI/Resources/Localizable.xcstrings"
CACHE = ROOT / "scripts/zh_hans_cache.json"
FORMAT = re.compile(r"%(?:\d+\$)?(?:lld|llu|ld|lu|zd|zu|lf|@|d|i|u|s|f|g|G|e|E|x|X|o|p|c)|%#@[^@]+@|%%")
GUARD = re.compile(r"__PINCER_FMT_(\d{4})__")
SEPARATOR = "\n###\n"
COMMON = {
"Chat":"聊天","Chats":"聊天","New chat":"新建聊天","Settings":"设置","Send":"发送",
"Cancel":"取消","Save":"保存","Close":"关闭","Done":"完成","Delete":"删除",
"Remove":"移除","Retry":"重试","Continue":"继续","Back":"返回","Next":"下一步",
"Edit":"编辑","Copy":"复制","Copied":"已复制","Search":"搜索","Clear":"清除",
"Connect":"连接","Disconnect":"断开连接","Connected":"已连接","Connecting…":"正在连接…",
"Reconnecting…":"正在重新连接…","Disconnected":"已断开连接","Offline":"离线",
"Online":"在线","Gateway":"网关","Gateway Settings":"网关设置","Gateway URL":"网关地址",
"Gateway token":"网关令牌","Gateway password":"网关密码","Agents":"智能体",
"Agent":"智能体","Skills":"技能","Tools":"工具","Memories":"记忆","Memory":"记忆",
"Sessions":"会话","Session":"会话","History":"历史记录","Notifications":"通知",
"Appearance":"外观","Theme":"主题","Light":"浅色","Dark":"深色","System":"跟随系统",
"Voice":"语音","Microphone":"麦克风","Attach files":"添加文件","Attach photos":"添加照片",
"Copy message":"复制消息","Reply":"回复","Stop":"停止","Stop generating":"停止生成",
"Thinking":"思考中","Working":"执行中","Running":"运行中","Completed":"已完成",
"Failed":"失败","Error":"错误","Errors":"错误","Logs":"日志","Approvals":"操作审批",
"Approval":"操作审批","Approve":"批准","Deny":"拒绝","Allow":"允许","Always Allow":"始终允许",
"Allowed":"已允许","Reject":"拒绝","Model":"模型","Models":"模型","Usage":"用量",
"Cost":"费用","Files":"文件","File":"文件","Refresh":"刷新","Loading…":"正在加载…",
"No results":"没有结果","Open":"打开","Help":"帮助","Status":"状态","Health":"运行状况",
"Schedule":"计划","Automations":"自动化任务","Cron":"定时任务","Commands":"命令",
"Submit":"提交","Apply":"应用","Reset":"重置","Yes":"是","No":"否","OK":"确定",
"About":"关于","Start":"开始","Today":"今天","Yesterday":"昨天",
"Try the Demo":"体验演示","Get Started":"开始使用","View details":"查看详情",
"Details":"详情","General":"通用","Privacy":"隐私","Security":"安全","Advanced":"高级",
"Not now":"暂不","Learn more":"了解更多","Log out":"退出登录",
"Add":"添加","Add Gateway":"添加网关","Add Gateway…":"添加网关…","Add Server":"添加服务器",
"Actions":"操作","Active":"活跃","Always":"始终","All Settings":"全部设置",
"All Channels":"全部频道","Archive":"归档","Archived":"已归档",
"Authentication":"身份验证","Authorization":"授权","Assistant":"助手",
"Attachment":"附件","Attachments":"附件","Automations…":"自动化任务…",
"Back":"返回","Bookmark":"书签","Bookmarks":"书签",
"Branch from Here":"从这里创建分支","Change Model…":"切换模型…",
"Channel":"频道","Channels":"频道","Chat Options":"聊天选项",
"Clear Cache":"清除缓存","Clear Search":"清除搜索","Clear Filters":"清除筛选",
"Command Palette…":"命令面板…","Compact Now":"立即压缩上下文",
"Connection":"连接","Connection timeout":"连接超时","Context":"上下文",
"Context Window":"上下文窗口","Conversation":"对话","Create":"创建",
"Current default":"当前默认","Daily":"每天","Default":"默认",
"Default agent":"默认智能体","Default model":"默认模型",
"Delete Agent":"删除智能体","Delete Group":"删除分组",
"Description":"描述","Device ID":"设备 ID","Devices":"设备","Devices…":"设备…",
"Dictation":"语音听写","Disabled":"已禁用","Discard":"放弃更改",
"Display name":"显示名称","Edit & Resend":"编辑并重新发送",
"Edit Last Message":"编辑上一条消息","Enabled":"已启用",
"Enter a name.":"请输入名称。","Enter the server's URL.":"请输入服务器地址。",
"Failed to send.":"发送失败。","Find a chat":"查找聊天",
"Find in Chat":"在聊天中查找","Finish":"完成",
"Gateway Logs":"网关日志","Gateway Settings…":"网关设置…",
"Health":"运行状况","Help":"帮助","Hide":"隐藏",
"History":"历史记录","Import":"导入","Export":"导出",
"Local":"本地","Location":"位置","Main":"主会话",
"Manage":"管理","Messages":"消息","More":"更多",
"Name":"名称","New":"新建","New Chat":"新建聊天",
"None":"无","Notification":"通知","Outbox":"待发送队列",
"Pending":"等待中","Pause":"暂停","Paused":"已暂停",
"Permission":"权限","Permissions":"权限","Plugin":"插件","Plugins":"插件",
"Provider":"提供商","Providers":"提供商","Queued":"已排队",
"Reconnect":"重新连接","Regenerate":"重新生成","Restore":"恢复",
"Resume":"继续","Run":"运行","Running":"运行中","Save Changes":"保存更改",
"Search Chats":"搜索聊天","Select":"选择","Send Message":"发送消息",
"Server":"服务器","Setup":"设置向导","Share":"分享","Show":"显示",
"Skill":"技能","Stop":"停止","Success":"成功",
"Task":"任务","Tasks":"任务","Token":"令牌","Tokens":"令牌",
"Tool":"工具","Tool Calls":"工具调用","Tool call":"工具调用",
"Unknown":"未知","Update":"更新","Upload":"上传",
"Waiting":"等待中","Warning":"警告","Workspace":"工作区",
"Workspace Files":"工作区文件","Saved":"已保存","Cancelled":"已取消",
"Approve %@" :"批准 %@","Send…":"发送…","Retry…":"重试…",
"Go to Chats":"前往聊天","Go Back":"返回","Get Started":"开始使用",
"No chats yet":"暂无聊天","Add Reaction":"添加表情回应",
"Copy Code":"复制代码","Copy Details":"复制详情","Copy Error":"复制错误",
"Copy Link":"复制链接","Copy Raw":"复制原始内容",
"Copy Thinking":"复制思考过程","Copy Tool Name":"复制工具名称",
"Copy diff":"复制差异","Copy file contents":"复制文件内容",
"Chat unavailable":"聊天不可用","Can’t connect to %@":"无法连接到 %@",
"Command Policy":"命令权限策略","Command Policy…":"命令权限策略…",
"Allow Once":"仅允许一次","Always ignored":"始终忽略",
"Approval History":"审批历史","Approval Not Found":"未找到审批记录",
"Dictate Message":"语音输入","Dictation Is Off":"听写功能已关闭",
"Failed — %@":"失败 — %@","Failed to send: %@":"发送失败：%@",
"Chat Color":"聊天颜色","Add Reaction…":"添加表情回应…",
"Copy Session Key":"复制会话密钥","Copy Device ID":"复制设备 ID",
"Copy Request ID":"复制请求 ID","Copy Setting Path":"复制设置路径",
"Copy Name":"复制名称","Copy ID":"复制 ID","Copy output":"复制输出",
"Copy command":"复制命令","Copy message":"复制消息",
"Discard Changes":"放弃更改","Delete unsent message":"删除未发送的消息",
"Confirm Plugin Change":"确认插件变更","Device Voice":"设备语音",
"Gateway Voice":"网关语音","Appearance":"外观",
}
def units(x):
    if isinstance(x, dict):
        if isinstance(x.get("stringUnit"), dict) and "value" in x["stringUnit"]:
            yield x["stringUnit"]
        for k,v in x.items():
            if k != "stringUnit":
                yield from units(v)
    elif isinstance(x, list):
        for v in x:
            yield from units(v)

def place(x):
    return collections.Counter(FORMAT.findall(x))

def protect(x):
    original=[]
    def sub(m):
        original.append(m.group())
        return "__PINCER_FMT_%04d__" % (len(original)-1)
    return FORMAT.sub(sub,x),original

def restore(x,orig):
    found=[]
    def sub(m):
        n=int(m.group(1))
        if n>=len(orig): raise ValueError("unknown placeholder")
        found.append(n)
        return orig[n]
    out=GUARD.sub(sub,x)
    if collections.Counter(found)!=collections.Counter(range(len(orig))):
        raise ValueError("placeholder dropped or duplicated")
    return out

def google_translate(text):
    # Use curl because public site may reject Python urllib user agents.
    cmd=["curl","-fsSL","--retry","2","--max-time","28","-G",
         "https://translate.google.com/translate_a/single",
         "--data-urlencode","client=gtx","--data-urlencode","sl=en",
         "--data-urlencode","tl=zh-CN","--data-urlencode","dt=t",
         "--data-urlencode","q="+text]
    result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    payload=json.loads(result.stdout)
    return "".join(x[0] or "" for x in payload[0])

def translate_group(items):
    enc=[protect(s) for s in items]
    response=google_translate(SEPARATOR.join(x[0] for x in enc))
    split=re.split(r"\n\s*###\s*\n",response)
    if len(split)!=len(items):
        raise ValueError("batch delimiter altered")
    result={}
    for s,orig,chunk in zip(items,enc,split):
        value=restore(chunk.strip(),orig[1])
        if place(s)!=place(value):
            raise ValueError("placeholder changed")
        result[s]=value
    return result

def populate(data,cache):
    count=0
    for entry in data["strings"].values():
        en=entry["localizations"]["en"]
        cn=copy.deepcopy(en)
        for x in units(cn):
            original=x["value"]
            new=COMMON.get(original,cache.get(original,original))
            if place(original)!=place(new):
                new=original
            x["value"]=new
            x["state"]="translated"
            count+=(new!=original)
        entry["localizations"]["zh-Hans"]=cn
    return count

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--max-batches",type=int,default=0,help="Limit network batches for a resumable translation pass")
    p.add_argument("--check",action="store_true")
    args=p.parse_args()
    data=json.loads(CAT.read_text(encoding="utf-8"))
    cached=json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    refs={}
    for key,entry in data["strings"].items():
        for unit in units(entry["localizations"]["en"]):
            refs[unit["value"]]=None
    texts=list(refs)
    if not args.check:
        todo=[s for s in texts if s not in cached and s not in COMMON and re.search(r"[A-Za-z]",s) and len(s)<750]
        print("Total",len(texts),"unique strings; translate online",len(todo),flush=True)
        groups=[];batch=[];chars=0
        for s in todo:
            if batch and (len(batch)>=6 or chars+len(s)>800):
                groups.append(batch);batch=[];chars=0
            batch.append(s);chars+=len(s)
        if batch: groups.append(batch)
        failures=0
        def run_group(group):
            try:
                return translate_group(group), False
            except Exception:
                partial={}
                for item in group:
                    try:
                        partial.update(translate_group([item]))
                    except Exception:
                        pass
                return partial, True

        if args.max_batches:
            groups=groups[:args.max_batches]
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures=[pool.submit(run_group,group) for group in groups]
            for i,future in enumerate(as_completed(futures),1):
                values,used_fallback=future.result()
                cached.update(values)
                failures+=int(used_fallback)
                if i%8==0:
                    CACHE.write_text(json.dumps(cached,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                if i%20==0:
                    print("Progress batches",i,"/",len(groups),"cache",len(cached),"failures",failures,flush=True)
        CACHE.write_text(json.dumps(cached,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    localized=populate(data,cached)
    if not args.check:
        CAT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    missing=[]; bad=[]; chinese=0; same=0; total=0
    for key,entry in data["strings"].items():
        target=entry["localizations"].get("zh-Hans")
        if target is None:
            missing.append(key);continue
        en=list(units(entry["localizations"]["en"])); zh=list(units(target))
        if len(en)!=len(zh): bad.append(key);continue
        for a,b in zip(en,zh):
            total+=1
            if place(a["value"])!=place(b["value"]):bad.append(key)
            if a["value"]==b["value"]:same+=1
            if re.search(r"[\u3400-\u9fff]",b["value"]):chinese+=1
    print("Locales:",len(data["strings"]),"entries; translated units",localized,
          "; CJK units",chinese,"/",total,"; same as English",same,
          "; format_errors",len(bad),"; missing",len(missing),flush=True)
    if missing or bad: raise SystemExit("Invalid translation resources")
if __name__=="__main__": main()

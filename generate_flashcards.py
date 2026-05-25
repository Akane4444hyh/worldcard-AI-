#!/usr/bin/env python3
"""Generate a single-HTML flashcard app — empty word bank, add words via import."""

import json
import os

HTML_PATH = "flashcards.html"

# ── Empty word bank ────────────────────────────────────
cards = []
cards_json = "[]"
total = 0

# ── HTML template ──────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>world-card</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif;
  background: #0f0a1a;
  color: #e8e0f0;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s, color 0.3s;
}}

.app {{
  display: flex;
  width: 100vw;
  height: 100vh;
}}

.sidebar {{
  width: 350px;
  background: #120d24;
  border-right: 1px solid #2d204a;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.3s, background 0.3s, border-color 0.3s;
}}
.sidebar.hidden {{
  width: 0;
  border-right: none;
}}
.sidebar.hidden > * {{ display: none; }}

.sidebar-inner {{
  display: flex;
  height: 100%;
  overflow: hidden;
}}

/* ── Group tabs column (left) ── */
.group-tabs-col {{
  width: 90px;
  min-width: 90px;
  background: #0d0820;
  border-right: 1px solid #2d204a;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 8px 6px;
  gap: 6px;
  transition: background 0.3s, border-color 0.3s;
}}
.group-tabs-col::-webkit-scrollbar {{ width: 2px; }}
.group-tabs-col::-webkit-scrollbar-thumb {{ background: #2d204a; border-radius: 1px; }}

.group-tab-v {{
  padding: 10px 6px;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  background: #120d24;
  border: 1px solid transparent;
  transition: all 0.2s;
  font-size: 12px;
  color: #8b8aaa;
  line-height: 1.4;
  word-break: break-all;
}}
.group-tab-v:hover {{
  border-color: #2d204a;
  color: #c4b5fd;
}}
.group-tab-v.active {{
  background: #7c3aed18;
  border-color: #a78bfa;
  color: #a78bfa;
}}
.group-tab-v .gt-name {{
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 4px;
  color: inherit;
}}
.group-tab-v .gt-counts {{
  font-size: 10px;
  opacity: 0.7;
  line-height: 1.5;
}}

/* ── Right content area ── */
.sidebar-content {{
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}}

.sidebar-header {{
  padding: 16px 14px;
  border-bottom: 1px solid #2d204a;
  font-size: 13px;
  color: #8b8aaa;
  letter-spacing: 0.3px;
  transition: border-color 0.3s, color 0.3s;
}}

.search-box {{
  margin: 12px;
  padding: 9px 14px;
  border: 1px solid #2d204a;
  border-radius: 10px;
  background: #0f0a1a;
  color: #e8e0f0;
  font-size: 13px;
  outline: none;
  transition: border-color 0.25s, box-shadow 0.25s, background 0.3s, color 0.3s;
}}
.search-box:focus {{ border-color: #a78bfa; box-shadow: 0 0 0 3px #a78bfa20; }}
.search-box::placeholder {{ color: #5a5880; }}

.word-list {{
  flex: 1;
  overflow-y: auto;
  padding: 0 6px 6px;
  user-select: none;
  -webkit-user-select: none;
}}
.word-list::-webkit-scrollbar {{ width: 4px; }}
.word-list::-webkit-scrollbar-thumb {{ background: #2d204a; border-radius: 2px; }}

.word-item {{
  padding: 9px 12px;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 1px;
  color: #c0b8d0;
}}
.word-item:hover {{ background: #1e1640; color: #e8e0f0; }}
.word-item.active {{ background: #a78bfa18; color: #a78bfa; font-weight: 600; }}

.main {{
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
}}

.topbar {{
  position: absolute;
  top: 24px;
  left: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}}

.topbar-group {{
  display: flex;
  align-items: center;
  gap: 8px;
}}

.toggle-btn {{
  background: #1a1230;
  border: 1px solid #2d204a;
  color: #a78bfa;
  padding: 8px 16px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.25s;
}}
.toggle-btn:hover {{ background: #251a40; border-color: #a78bfa; box-shadow: 0 0 12px #a78bfa15; }}

.progress {{
  font-size: 15px;
  color: #8b8aaa;
  font-weight: 500;
}}
.progress span {{ color: #a78bfa; font-weight: 700; }}

.card-container {{
  perspective: 1000px;
  width: 520px;
  height: 380px;
  margin: 40px 0 30px;
}}

.card {{
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}}
.card.flipped {{ transform: rotateY(180deg); }}

.card-face {{
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid #2d204a;
  box-shadow: 0 8px 32px #00000040, 0 0 60px #7c3aed10;
  transition: background 0.3s, border-color 0.3s, box-shadow 0.3s;
}}

.card-front {{
  background: linear-gradient(135deg, #1a1230 0%, #1e1640 100%);
}}
.card-front .word {{
  font-size: 3.4rem;
  font-weight: 700;
  color: #c4b5fd;
  text-shadow: 0 0 20px #a78bfa20;
  letter-spacing: 1px;
  transition: color 0.3s, text-shadow 0.3s;
}}

.card-back {{
  background: linear-gradient(135deg, #1a1230 0%, #1e1640 100%);
  transform: rotateY(180deg);
  padding: 36px;
  overflow-y: auto;
}}
.card-back .meaning {{
  font-size: 1.4rem;
  color: #e8e0f0;
  margin-bottom: 18px;
  line-height: 1.7;
  text-align: center;
}}
.card-back .phrases-title {{
  font-size: 13px;
  color: #8b8aaa;
  margin-bottom: 10px;
  text-align: center;
}}
.card-back .phrase-item {{
  font-size: 13px;
  color: #8b8aaa;
  padding: 6px 0;
  border-bottom: 1px solid #2d204a;
  text-align: center;
}}
.card-back .phrase-item:last-child {{ border-bottom: none; }}
.card-back .phrase-highlight {{ color: #c4b5fd; }}

.nav {{
  display: flex;
  align-items: center;
  gap: 28px;
}}

.nav-btn {{
  background: #1a1230;
  border: 1px solid #2d204a;
  color: #c4b5fd;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  font-size: 22px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s;
}}
.nav-btn:hover {{ background: #7c3aed; border-color: #7c3aed; color: #fff; box-shadow: 0 0 20px #7c3aed40; transform: translateY(-2px); }}
.nav-btn:active {{ transform: scale(0.93); }}

.nav-btn.flip-btn {{
  width: 64px;
  height: 64px;
  background: #7c3aed;
  border: none;
  color: #fff;
  font-size: 24px;
  box-shadow: 0 4px 20px #7c3aed30;
}}
.nav-btn.flip-btn:hover {{ background: #8b5cf6; box-shadow: 0 6px 28px #7c3aed50; }}

.nav-btn.slay-btn {{
  background: linear-gradient(135deg, #be123c, #e11d48);
  border: none;
  color: #fdf5e6;
  font-size: 18px;
  font-weight: 700;
  box-shadow: 0 4px 20px #e11d4820;
}}
.nav-btn.slay-btn:hover {{ background: linear-gradient(135deg, #e11d48, #f43f5e); box-shadow: 0 6px 28px #e11d4840; }}

.sidebar-footer {{
  padding: 10px;
  border-top: 1px solid #2d204a;
  transition: border-color 0.3s;
}}
.sidebar-footer .toggle-btn {{
  width: 100%;
  text-align: center;
  font-size: 12px;
  padding: 8px;
}}

.word-item.slain {{
  opacity: 0.35;
  text-decoration: line-through;
  cursor: pointer;
}}
.word-item.slain:hover {{ opacity: 0.7; background: #2d1140; }}

.empty-state {{
  text-align: center;
  display: none;
}}
.empty-state.show {{ display: block; }}
.empty-state .empty-title {{
  font-size: 2rem;
  font-weight: 700;
  color: #c4b5fd;
  margin-bottom: 12px;
}}
.empty-state .empty-sub {{
  font-size: 1rem;
  color: #8b8aaa;
  margin-bottom: 24px;
}}

.modal-overlay {{
  display: none;
  position: fixed;
  inset: 0;
  background: #00000070;
  backdrop-filter: blur(4px);
  z-index: 100;
  align-items: center;
  justify-content: center;
}}
.modal-overlay.show {{ display: flex; }}

.modal {{
  background: #1a1230;
  border: 1px solid #2d204a;
  border-radius: 16px;
  padding: 28px;
  width: 90vw;
  max-width: 520px;
  box-shadow: 0 16px 48px #00000060;
  transition: background 0.3s, border-color 0.3s, box-shadow 0.3s;
}}
.modal h3 {{
  font-size: 1.1rem;
  color: #c4b5fd;
  margin-bottom: 6px;
}}
.modal .modal-desc {{
  font-size: 13px;
  color: #8b8aaa;
  margin-bottom: 16px;
  line-height: 1.5;
}}
.modal textarea {{
  width: 100%;
  height: 200px;
  background: #0f0a1a;
  border: 1px solid #2d204a;
  border-radius: 12px;
  color: #e8e0f0;
  padding: 14px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  transition: border-color 0.25s, background 0.3s, color 0.3s;
}}
.modal textarea:focus {{ border-color: #a78bfa; }}
.modal .modal-actions {{
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 16px;
}}
.modal .modal-actions .toggle-btn {{
  font-size: 13px;
}}
.modal .group-input {{
  width: 100%;
  padding: 10px 14px;
  background: #0f0a1a;
  border: 1px solid #2d204a;
  border-radius: 12px;
  color: #e8e0f0;
  font-size: 14px;
  outline: none;
  margin-bottom: 12px;
  transition: border-color 0.25s, background 0.3s, color 0.3s;
}}
.modal .group-input:focus {{ border-color: #a78bfa; }}
.modal .file-upload {{
  margin-bottom: 12px;
}}
.modal .file-upload label {{
  display: block;
  font-size: 13px;
  color: #8b8aaa;
  margin-bottom: 6px;
}}
.modal .file-upload input[type="file"] {{
  width: 100%;
  padding: 10px;
  background: #0f0a1a;
  border: 1px solid #2d204a;
  border-radius: 12px;
  color: #8b8aaa;
  font-size: 13px;
  cursor: pointer;
}}
.modal .file-upload input[type="file"]::file-selector-button {{
  background: #1a1230;
  border: 1px solid #2d204a;
  border-radius: 8px;
  color: #a78bfa;
  padding: 6px 14px;
  cursor: pointer;
  font-size: 13px;
  margin-right: 10px;
}}

.word-item.slain.drag-hover {{
  opacity: 0.7;
  background: #3d1a50;
  border: 1px solid #a78bfa;
}}

.word-item .slain-cb {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1.5px solid #4a4570;
  margin-right: 8px;
  flex-shrink: 0;
  transition: all 0.2s;
  font-size: 10px;
  color: transparent;
  vertical-align: middle;
}}
.word-item.slain .slain-cb.checked {{
  background: #a78bfa;
  border-color: #a78bfa;
  color: #fff;
}}

.batch-restore-bar {{
  display: none;
  padding: 8px 12px;
  border-top: 1px solid #2d204a;
  gap: 8px;
  align-items: center;
  transition: border-color 0.3s;
}}
.batch-restore-bar.show {{ display: flex; }}
.batch-restore-bar .select-all-text {{
  font-size: 11px;
  color: #8b8aaa;
  cursor: pointer;
  user-select: none;
}}
.batch-restore-bar .select-all-text:hover {{ color: #a78bfa; }}

.reset-btn {{
  background: #1a1230;
  border: 1px solid #3d2840;
  color: #6b5070;
  padding: 8px 16px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.25s;
}}
.reset-btn:hover {{ border-color: #e11d48; color: #e11d48; box-shadow: 0 0 12px #e11d4810; }}

.confirm-modal {{
  text-align: center;
}}
.confirm-modal p {{
  font-size: 14px;
  color: #8b8aaa;
  margin: 16px 0 20px;
  line-height: 1.6;
}}

.hint {{
  font-size: 13px;
  color: #4a4570;
  position: absolute;
  bottom: 20px;
}}

/* ═══════════════════════════════════════════
   Light mode — pink-white theme
   ═══════════════════════════════════════════ */
body.light {{
  background: #fef9fa;
  color: #4a3548;
}}
body.light .sidebar {{
  background: #fff5f7;
  border-right-color: #f0d4dc;
}}
body.light .group-tabs-col {{
  background: #fce4ec;
  border-right-color: #f0d4dc;
}}
body.light .group-tab-v {{
  background: #fff0f3;
  color: #8b6a7a;
}}
body.light .group-tab-v:hover {{
  border-color: #f0b8c8;
  color: #4a3548;
}}
body.light .group-tab-v.active {{
  background: #f8bbd020;
  border-color: #e91e63;
  color: #e91e63;
}}
body.light .sidebar-header {{
  border-bottom-color: #f0d4dc;
  color: #8b6a7a;
}}
body.light .search-box {{
  background: #fff;
  border-color: #f0d4dc;
  color: #4a3548;
}}
body.light .search-box:focus {{
  border-color: #e91e63;
  box-shadow: 0 0 0 3px #e91e6320;
}}
body.light .search-box::placeholder {{ color: #c0a8b4; }}
body.light .word-item {{ color: #6a5a68; }}
body.light .word-item:hover {{ background: #fce4ec; color: #4a3548; }}
body.light .word-item.active {{ background: #f8bbd018; color: #e91e63; }}
body.light .word-item.slain:hover {{ background: #f8bbd0; }}
body.light .word-item.slain.drag-hover {{
  background: #f8bbd0;
  border-color: #e91e63;
}}
body.light .word-item .slain-cb {{ border-color: #c0a8b4; }}
body.light .word-item.slain .slain-cb.checked {{
  background: #e91e63;
  border-color: #e91e63;
  color: #fff;
}}
body.light .card-front {{
  background: #fff;
}}
body.light .card-front .word {{
  color: #e91e63;
  text-shadow: none;
}}
body.light .card-back {{
  background: #fff;
}}
body.light .card-face {{
  border-color: #f0d4dc;
  box-shadow: 0 8px 32px #00000010, 0 0 60px #e91e6308;
}}
body.light .card-back .meaning {{ color: #4a3548; }}
body.light .card-back .phrases-title {{ color: #8b6a7a; }}
body.light .card-back .phrase-item {{
  color: #8b6a7a;
  border-bottom-color: #f0d4dc;
}}
body.light .card-back .phrase-highlight {{ color: #e91e63; }}
body.light .nav-btn {{
  background: #fff;
  border-color: #f0d4dc;
  color: #e91e63;
}}
body.light .nav-btn:hover {{
  background: #e91e63;
  border-color: #e91e63;
  color: #fff;
  box-shadow: 0 0 20px #e91e6340;
}}
body.light .nav-btn.flip-btn {{
  background: #e91e63;
  color: #fff;
  box-shadow: 0 4px 20px #e91e6330;
}}
body.light .nav-btn.flip-btn:hover {{
  background: #c2185b;
  box-shadow: 0 6px 28px #e91e6350;
}}
body.light .nav-btn.slay-btn {{
  background: #ec407a;
  color: #fdf5e6;
}}
body.light .nav-btn.slay-btn:hover {{
  background: #d81b60;
}}
body.light .toggle-btn {{
  background: #fff;
  border-color: #f0d4dc;
  color: #e91e63;
}}
body.light .toggle-btn:hover {{
  background: #fff0f3;
  border-color: #e91e63;
  box-shadow: 0 0 12px #e91e6315;
}}
body.light .progress {{ color: #8b6a7a; }}
body.light .progress span {{ color: #e91e63; }}
body.light .hint {{ color: #c0a8b4; }}
body.light .modal-overlay {{ background: #00000030; }}
body.light .modal {{
  background: #fff;
  border-color: #f0d4dc;
  box-shadow: 0 16px 48px #00000015;
}}
body.light .modal h3 {{ color: #e91e63; }}
body.light .modal .modal-desc {{ color: #8b6a7a; }}
body.light .modal textarea {{
  background: #fef9fa;
  border-color: #f0d4dc;
  color: #4a3548;
}}
body.light .modal textarea:focus {{ border-color: #e91e63; }}
body.light .modal .group-input {{
  background: #fef9fa;
  border-color: #f0d4dc;
  color: #4a3548;
}}
body.light .modal .group-input:focus {{ border-color: #e91e63; }}
body.light .modal .file-upload label {{ color: #8b6a7a; }}
body.light .modal .file-upload input[type="file"] {{
  background: #fef9fa;
  border-color: #f0d4dc;
  color: #8b6a7a;
}}
body.light .modal .file-upload input[type="file"]::file-selector-button {{
  background: #fff;
  border-color: #f0d4dc;
  color: #e91e63;
}}
body.light .batch-restore-bar {{ border-top-color: #f0d4dc; }}
body.light .batch-restore-bar .select-all-text {{ color: #8b6a7a; }}
body.light .batch-restore-bar .select-all-text:hover {{ color: #e91e63; }}
body.light .reset-btn {{
  background: #fff;
  border-color: #f0d4dc;
  color: #8b6a7a;
}}
body.light .reset-btn:hover {{
  border-color: #e91e63;
  color: #e91e63;
  box-shadow: 0 0 12px #e91e6310;
}}
body.light .sidebar-footer {{ border-top-color: #f0d4dc; }}
body.light .empty-state .empty-title {{ color: #e91e63; }}
body.light .empty-state .empty-sub {{ color: #8b6a7a; }}
body.light .confirm-modal p {{ color: #8b6a7a; }}
body.light .word-list::-webkit-scrollbar-thumb {{ background: #f0d4dc; }}
body.light .group-tabs-col::-webkit-scrollbar-thumb {{ background: #f0d4dc; }}

@media (max-width: 768px) {{
  .sidebar {{ display: none; }}
  .card-container {{ width: 90vw; height: 300px; }}
  .card-front .word {{ font-size: 2rem; }}
  .card-back .meaning {{ font-size: 1.1rem; }}
  .topbar {{ flex-wrap: wrap; gap: 8px; }}
  .toggle-btn {{ padding: 6px 12px; font-size: 12px; }}
}}
</style>
</head>
<body>
<div class="app">
  <!-- Sidebar -->
  <aside class="sidebar hidden" id="sidebar">
    <div class="sidebar-inner">
      <!-- Left: vertical group tabs -->
      <div class="group-tabs-col" id="groupTabsCol"></div>
      <!-- Right: content area -->
      <div class="sidebar-content">
        <div class="sidebar-header">未斩 <span id="remainingCount">{total}</span> · 已斩 <span id="slainCount">0</span></div>
        <input class="search-box" id="searchBox" placeholder="在当前分组中搜索…" autocomplete="off">
        <div class="word-list" id="wordList"></div>
        <div class="batch-restore-bar" id="batchRestoreBar">
          <span class="select-all-text" id="selectAllSlain">全选</span>
          <span class="select-all-text" id="deselectAllSlain">取消</span>
          <div style="flex:1"></div>
          <button class="toggle-btn" id="restoreSelectedBtn" style="font-size:12px;padding:6px 14px;">恢复选中 (<span id="selectedSlainCount">0</span>)</button>
        </div>
        <div class="sidebar-footer" style="display:flex;flex-direction:column;gap:6px;">
          <button class="toggle-btn" id="restoreAllBtn">恢复全部已斩</button>
          <button class="toggle-btn" id="deleteGroupBtn" style="display:none;color:#e11d48;border-color:#e11d4820;">删除当前分组</button>
          <button class="reset-btn" id="resetAllBtn">重置所有数据</button>
        </div>
      </div>
    </div>
  </aside>

  <!-- Main area -->
  <main class="main">
    <div class="topbar">
      <div class="topbar-group">
        <button class="toggle-btn" id="toggleSidebar">列表</button>
        <button class="toggle-btn" id="shuffleBtn" title="打乱顺序">打乱</button>
        <button class="toggle-btn" id="resetOrderBtn" title="恢复默认顺序">恢复</button>
        <button class="toggle-btn" id="importBtn" title="导入单词">导入</button>
      </div>
      <div style="display:flex;align-items:center;gap:10px;">
        <button class="toggle-btn" id="themeBtn" title="切换亮色/暗色模式">亮色</button>
        <div class="progress" id="progressBar"><span id="currentNum">0</span> / <span id="totalRemaining">0</span></div>
      </div>
    </div>

    <div class="card-container" id="cardContainer">
      <div class="empty-state" id="emptyState">
        <div class="empty-title">还没有单词</div>
        <div class="empty-sub">点击「导入」按钮添加单词，支持 .json / .txt 格式</div>
        <button class="toggle-btn" id="emptyImportBtn">开始导入</button>
      </div>
      <div class="card" id="card">
        <div class="card-face card-front">
          <div class="word" id="wordDisplay">loading…</div>
        </div>
        <div class="card-face card-back" id="cardBack">
          <div class="meaning" id="meaningDisplay"></div>
          <div class="phrases-title" id="phrasesTitle"></div>
          <div id="phrasesList"></div>
        </div>
      </div>
    </div>

    <div class="nav" id="navBar">
      <button class="nav-btn" id="prevBtn" title="上一个 (←)">←</button>
      <button class="nav-btn flip-btn" id="flipBtn" title="翻转 (空格)">⟳</button>
      <button class="nav-btn" id="nextBtn" title="下一个 (→)">→</button>
      <button class="nav-btn slay-btn" id="slayBtn" title="斩杀此词 (K)">斩</button>
    </div>

    <div class="hint">← → 翻页 · 空格/点击 翻转 · K 斩杀 · R 恢复顺序 · 输入即搜索</div>

    <!-- Import modal -->
    <div class="modal-overlay" id="importModal">
      <div class="modal">
        <h3>导入单词</h3>
        <div class="modal-desc">支持上传 .json / .txt 文件，或手动粘贴内容</div>
        <input class="group-input" id="importGroupName" placeholder="分组名（必填，同名归入已有组）" autocomplete="off" required>
        <div class="file-upload">
          <label>选择文件（.json / .txt）</label>
          <input type="file" id="importFileInput" accept=".json,.txt" multiple>
        </div>
        <textarea id="importTextarea" placeholder="abandon — v. 放弃&#10;abuse — v. 滥用, n. 虐待&#10;..." style="height:140px;"></textarea>
        <div class="modal-actions">
          <button class="toggle-btn" id="cancelImportBtn">取消</button>
          <button class="toggle-btn" id="confirmImportBtn" style="background:#7c3aed;border-color:#7c3aed;color:#fff;">导入</button>
        </div>
      </div>
    </div>

    <!-- Reset confirmation modal -->
    <div class="modal-overlay" id="resetModal">
      <div class="modal confirm-modal">
        <h3>重置所有数据</h3>
        <p>这将清除所有导入的单词、分组、斩杀记录和顺序设置。<br>此操作不可撤销。</p>
        <div class="modal-actions">
          <button class="toggle-btn" id="cancelResetBtn">取消</button>
          <button class="toggle-btn" id="confirmResetBtn" style="background:#e11d48;border-color:#e11d48;color:#fff;">确认重置</button>
        </div>
      </div>
    </div>
  </main>
</div>

<script>
// ── Data ──
let CARDS = {cards_json};
const BUILTIN_TOTAL = CARDS.length;

let customWords = (() => {{
  const saved = localStorage.getItem('cet6-custom');
  if (saved) {{ try {{ return JSON.parse(saved); }} catch(e) {{}} }}
  return [];
}})();
if (customWords.length > 0) CARDS = CARDS.concat(customWords);

let slain = new Set((() => {{
  const saved = localStorage.getItem('cet6-slain');
  if (saved) {{ try {{ return JSON.parse(saved); }} catch(e) {{}} }}
  return [];
}})());

// Group list derived from custom words
function getGroups() {{
  const groups = new Set();
  for (const c of customWords) {{ if (c.group) groups.add(c.group); }}
  return [...groups];
}}

function saveSlain() {{ localStorage.setItem('cet6-slain', JSON.stringify([...slain])); }}
function saveCustom() {{ localStorage.setItem('cet6-custom', JSON.stringify(customWords)); }}

// ── Order: indices of unslain cards ──
function rebuildOrder() {{
  const shuffled = localStorage.getItem('cet6-shuffled');
  if (shuffled) {{
    try {{
      const saved = JSON.parse(shuffled);
      // Filter out invalid indices (CARDS shrinks after group deletion)
      const validSaved = saved.filter(i => i >= 0 && i < CARDS.length);
      const savedSet = new Set(validSaved);
      const filtered = validSaved.filter(i => !slain.has(i));
      // New cards not in saved sequence: append alphabetically
      const newOnes = [];
      for (let i = 0; i < CARDS.length; i++) {{
        if (!slain.has(i) && !savedSet.has(i)) newOnes.push(i);
      }}
      newOnes.sort((a, b) => CARDS[a].word.toLowerCase().localeCompare(CARDS[b].word.toLowerCase()));
      return [...filtered, ...newOnes];
    }} catch(e) {{}}
  }}
  const arr = [];
  for (let i = 0; i < CARDS.length; i++) {{ if (!slain.has(i)) arr.push(i); }}
  arr.sort((a, b) => CARDS[a].word.toLowerCase().localeCompare(CARDS[b].word.toLowerCase()));
  return arr;
}}

let order = rebuildOrder();

// ── State ──
let index = 0;           // position within current group's order
let flipped = false;
let activeGroup = null;  // set by buildGroupTabs on init
let slainChecked = new Set();

// ── Get order filtered by active group ──
function getGroupOrder() {{
  if (!activeGroup) return [...order];
  return order.filter(i => CARDS[i].group === activeGroup);
}}

// ── DOM refs ──
const card = document.getElementById('card');
const cardContainer = document.getElementById('cardContainer');
const emptyState = document.getElementById('emptyState');
const wordDisplay = document.getElementById('wordDisplay');
const meaningDisplay = document.getElementById('meaningDisplay');
const phrasesTitle = document.getElementById('phrasesTitle');
const phrasesList = document.getElementById('phrasesList');
const currentNum = document.getElementById('currentNum');
const totalRemaining = document.getElementById('totalRemaining');
const wordList = document.getElementById('wordList');
const searchBox = document.getElementById('searchBox');
const sidebar = document.getElementById('sidebar');
const navBar = document.getElementById('navBar');
const remainingCount = document.getElementById('remainingCount');
const slainCount = document.getElementById('slainCount');
const groupTabsCol = document.getElementById('groupTabsCol');
const batchRestoreBar = document.getElementById('batchRestoreBar');

function countGroup(groupName) {{
  let unslawn = 0, slawn = 0;
  for (let i = 0; i < CARDS.length; i++) {{
    if (CARDS[i].group !== groupName) continue;
    if (slain.has(i)) slawn++; else unslawn++;
  }}
  return {{ unslawn, slawn }};
}}

function updateCounts() {{
  const gOrder = getGroupOrder();
  totalRemaining.textContent = gOrder.length;
  currentNum.textContent = gOrder.length > 0 ? index + 1 : 0;

  if (activeGroup) {{
    const c = countGroup(activeGroup);
    remainingCount.textContent = c.unslawn;
    slainCount.textContent = c.slawn;
  }} else {{
    remainingCount.textContent = order.length;
    slainCount.textContent = slain.size;
  }}
  buildGroupTabs();
}}

function checkEmpty() {{
  const gOrder = getGroupOrder();
  if (gOrder.length === 0) {{
    card.style.display = 'none';
    navBar.style.display = 'none';
    emptyState.classList.add('show');
  }} else {{
    card.style.display = '';
    navBar.style.display = '';
    emptyState.classList.remove('show');
  }}
}}

// ── Vertical group tabs ──
function buildGroupTabs() {{
  let groups = getGroups();
  if (groups.length === 0) {{
    groupTabsCol.innerHTML = '';
    document.getElementById('deleteGroupBtn').style.display = 'none';
    return;
  }}
  if (!activeGroup || !groups.includes(activeGroup)) activeGroup = groups[0];

  let html = '';
  for (const g of groups) {{
    const c = countGroup(g);
    const activeCls = activeGroup === g ? ' active' : '';
    html += `<div class="group-tab-v${{activeCls}}" data-group="${{g.replace(/"/g, '&quot;')}}">
      <div class="gt-name">${{g}}</div>
      <div class="gt-counts">未斩 ${{c.unslawn}}<br>已斩 ${{c.slawn}}</div>
    </div>`;
  }}
  groupTabsCol.innerHTML = html;

  const delBtn = document.getElementById('deleteGroupBtn');
  delBtn.style.display = '';
  delBtn.textContent = '删除分组: ' + activeGroup;
}}

function filterByGroup(groupName) {{
  activeGroup = groupName;
  index = 0;
  flipped = false;
  card.classList.remove('flipped');
  slainChecked.clear();
  buildGroupTabs();
  buildWordList(searchBox.value);
  updateBatchRestoreBar();
  renderCard();
}}

// ── Card rendering ──
function renderCard() {{
  const gOrder = getGroupOrder();
  if (gOrder.length === 0) {{
    checkEmpty();
    updateCounts();
    buildWordList(searchBox.value);
    return;
  }}
  checkEmpty();
  if (index >= gOrder.length) index = gOrder.length - 1;
  if (index < 0) index = 0;

  const c = CARDS[gOrder[index]];
  wordDisplay.textContent = c.word;
  meaningDisplay.textContent = c.meaning;

  if (c.phrases && c.phrases.length > 0) {{
    phrasesTitle.textContent = '短语 & 例句';
    phrasesList.innerHTML = c.phrases.map(p => {{
      const parts = p.split(' — ');
      return `<div class="phrase-item"><span class="phrase-highlight">${{parts[0]}}</span> — ${{parts[1] || ''}}</div>`;
    }}).join('');
  }} else {{
    phrasesTitle.textContent = '';
    phrasesList.innerHTML = '';
  }}

  updateCounts();
  buildWordList(searchBox.value);
}}

function flip() {{
  if (getGroupOrder().length === 0) return;
  flipped = !flipped;
  card.classList.toggle('flipped', flipped);
}}

function next() {{
  const gOrder = getGroupOrder();
  if (index < gOrder.length - 1) {{
    index++; flipped = false;
    card.classList.remove('flipped');
    renderCard();
  }}
}}

function prev() {{
  if (index > 0) {{
    index--; flipped = false;
    card.classList.remove('flipped');
    renderCard();
  }}
}}

function goTo(groupIdx) {{
  const gOrder = getGroupOrder();
  if (gOrder.length === 0) return;
  index = Math.max(0, Math.min(gOrder.length - 1, groupIdx));
  flipped = false;
  card.classList.remove('flipped');
  renderCard();
}}

// ── Slay word ──
function slayWord() {{
  const gOrder = getGroupOrder();
  if (gOrder.length === 0) return;
  const cardIndex = gOrder[index];
  slain.add(cardIndex);
  saveSlain();
  // Remove from global order
  const globalPos = order.indexOf(cardIndex);
  if (globalPos >= 0) order.splice(globalPos, 1);
  // Adjust group-relative position
  if (index >= gOrder.length - 1 && gOrder.length > 1) index = gOrder.length - 2;
  else if (gOrder.length === 1) index = 0;
  flipped = false;
  card.classList.remove('flipped');
  slainChecked.clear();
  renderCard();
}}

// ── Restore single word ──
function restoreWord(cardIndex) {{
  slain.delete(cardIndex);
  saveSlain();
  order = rebuildOrder();
  // Try to keep position within the same group
  const gOrder = getGroupOrder();
  const pos = gOrder.indexOf(cardIndex);
  if (pos >= 0) index = pos; else index = 0;
  flipped = false;
  card.classList.remove('flipped');
  slainChecked.delete(cardIndex);
  renderCard();
}}

// ── Restore all slain in current group ──
function restoreAll() {{
  const allSlain = [...slain].filter(i => CARDS[i].group === activeGroup);
  for (const ci of allSlain) slain.delete(ci);
  saveSlain();
  order = rebuildOrder();
  index = 0;
  flipped = false;
  card.classList.remove('flipped');
  slainChecked.clear();
  renderCard();
}}

// ── Batch restore ──
function toggleSlainCheck(cardIndex) {{
  if (slainChecked.has(cardIndex)) slainChecked.delete(cardIndex);
  else slainChecked.add(cardIndex);
  buildWordList(searchBox.value);
  updateBatchRestoreBar();
}}

function selectAllVisibleSlain() {{
  const f = searchBox.value.toLowerCase();
  for (let ci = 0; ci < CARDS.length; ci++) {{
    if (!slain.has(ci)) continue;
    if (activeGroup !== null) {{
      const c = CARDS[ci];
      if (!c.group || c.group !== activeGroup) continue;
    }}
    const c = CARDS[ci];
    if (f && !c.word.toLowerCase().includes(f)) continue;
    slainChecked.add(ci);
  }}
  buildWordList(f);
  updateBatchRestoreBar();
}}

function deselectAllSlain() {{
  slainChecked.clear();
  buildWordList(searchBox.value);
  updateBatchRestoreBar();
}}

function restoreSelected() {{
  if (slainChecked.size === 0) return;
  for (const ci of slainChecked) slain.delete(ci);
  saveSlain();
  order = rebuildOrder();
  if (getGroupOrder().length > 0) index = 0;
  slainChecked.clear();
  flipped = false;
  card.classList.remove('flipped');
  renderCard();
  buildGroupTabs();
}}

function updateBatchRestoreBar() {{
  const bar = batchRestoreBar;
  const count = slainChecked.size;
  document.getElementById('selectedSlainCount').textContent = count;
  if (count > 0) bar.classList.add('show');
  else bar.classList.remove('show');
}}

// ── Display sequence for sidebar: current group's unslain + slain ──
function getDisplaySequence() {{
  if (!activeGroup) {{
    const seq = [...order];
    const slainArr = [...slain].sort((a, b) =>
      CARDS[a].word.toLowerCase().localeCompare(CARDS[b].word.toLowerCase())
    );
    seq.push(...slainArr);
    return seq;
  }}
  // Only show words from the active group
  const gOrder = getGroupOrder();
  const seq = [...gOrder];
  const gSlain = [];
  for (const si of slain) {{
    if (CARDS[si].group === activeGroup) gSlain.push(si);
  }}
  gSlain.sort((a, b) =>
    CARDS[a].word.toLowerCase().localeCompare(CARDS[b].word.toLowerCase())
  );
  seq.push(...gSlain);
  return seq;
}}

// ── Sidebar word list ──
function buildWordList(filter = '') {{
  const f = filter.toLowerCase();
  const seq = getDisplaySequence();
  const gOrder = getGroupOrder();

  wordList.innerHTML = seq
    .map((ci) => {{
      const c = CARDS[ci];
      const isSlain = slain.has(ci);
      const groupPos = gOrder.indexOf(ci);
      const isActive = groupPos >= 0 && groupPos === index;
      let cls = 'word-item';
      if (isActive) cls += ' active';
      if (isSlain) cls += ' slain';

      let cbHtml = '';
      if (isSlain) {{
        const checked = slainChecked.has(ci) ? ' checked' : '';
        cbHtml = `<span class="slain-cb${{checked}}" data-cb="${{ci}}">${{checked ? '✓' : ''}}</span>`;
      }}

      const display = !f || c.word.toLowerCase().includes(f) ? '' : 'style="display:none"';
      return `<div class="${{cls}}" data-card-idx="${{ci}}" data-order-idx="${{groupPos}}" ${{display}}>${{cbHtml}}${{c.word}}</div>`;
    }})
    .join('');
}}

// ── Alphabetical sort ──
function alphaSortAll() {{
  const allIndices = Array.from({{length: CARDS.length}}, (_, i) => i);
  allIndices.sort((a, b) => CARDS[a].word.toLowerCase().localeCompare(CARDS[b].word.toLowerCase()));
  order = allIndices.filter(i => !slain.has(i));
  localStorage.setItem('cet6-shuffled', JSON.stringify(allIndices));
}}

function sortOrderAlphabetically() {{
  alphaSortAll();
}}

// ── Shuffle ──
function shuffleOrder() {{
  for (let i = order.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [order[i], order[j]] = [order[j], order[i]];
  }}
  const slainArr = [...slain].sort((a, b) =>
    CARDS[a].word.toLowerCase().localeCompare(CARDS[b].word.toLowerCase())
  );
  localStorage.setItem('cet6-shuffled', JSON.stringify([...order, ...slainArr]));
  index = 0; flipped = false;
  card.classList.remove('flipped');
  renderCard();
}}

function resetOrder() {{
  alphaSortAll();
  index = 0; flipped = false;
  card.classList.remove('flipped');
  renderCard();
}}

// ── Import ──
function showImportModal() {{
  document.getElementById('importModal').classList.add('show');
  document.getElementById('importGroupName').focus();
}}

function hideImportModal() {{
  document.getElementById('importModal').classList.remove('show');
  document.getElementById('importTextarea').value = '';
  document.getElementById('importGroupName').value = '';
  document.getElementById('importFileInput').value = '';
}}

function parseTXT(text) {{
  const cards = [];
  const lines = text.replace(/\\r\\n/g, '\\n').split('\\n').filter(l => l.trim());
  for (const line of lines) {{
    let word, meaning;
    if (line.includes(' — ')) {{
      [word, meaning] = line.split(' — ', 2);
    }} else if (line.includes(' | ')) {{
      [word, meaning] = line.split(' | ', 2);
    }} else if (line.includes('\t')) {{
      [word, meaning] = line.split('\t', 2);
    }} else {{
      const idx = line.indexOf(' ');
      if (idx > 0) {{ word = line.substring(0, idx); meaning = line.substring(idx + 1); }}
      else continue;
    }}
    word = word.trim(); meaning = meaning.trim();
    if (word && meaning) cards.push({{ word, meaning, phrases: [] }});
  }}
  return cards;
}}

function parseJSON(text) {{
  try {{
    const data = JSON.parse(text);
    const items = Array.isArray(data) ? data : (data.words || data.cards || data.data || []);
    return items.map(it => {{
      let meaning = '';
      // CET-6 format: translations: [{{type, translation}}]
      if (it.translations && Array.isArray(it.translations)) {{
        meaning = it.translations.map(t => (t.type ? t.type + '. ' : '') + t.translation).join(' | ');
      }} else {{
        meaning = it.meaning || it.translation || it.definition || '';
      }}
      let phrases = [];
      if (it.phrases && Array.isArray(it.phrases)) {{
        if (it.phrases.length > 0 && typeof it.phrases[0] === 'object') {{
          phrases = it.phrases.map(p => (p.phrase || '') + ' — ' + (p.translation || ''));
        }} else {{
          phrases = it.phrases;
        }}
      }}
      return {{ word: it.word || '', meaning, phrases }};
    }}).filter(it => it.word && it.meaning);
  }} catch(e) {{ console.warn('JSON parse error:', e.message); return []; }}
}}

function detectAndParse(text) {{
  const t = text.trim();
  if (!t) return [];
  if (t.startsWith('{{') || t.startsWith('[')) return parseJSON(t);
  return parseTXT(t);
}}

function addCardsToPool(newCards, groupName) {{
  let added = 0;
  for (const nc of newCards) {{
    // Only check for duplicates within the same group
    const existingIdx = CARDS.findIndex(c => c.word.toLowerCase() === nc.word.toLowerCase() && c.group === groupName);
    if (existingIdx >= 0) {{
      const existing = CARDS[existingIdx];
      // Same word, same group: override meaning if different
      if (existing.meaning !== nc.meaning) {{
        existing.meaning = nc.meaning;
        existing.phrases = nc.phrases || [];
        added++;
      }}
      continue;
    }}
    const card = {{ word: nc.word, meaning: nc.meaning, phrases: nc.phrases || [], group: groupName }};
    CARDS.push(card);
    customWords.push(card);
    order.push(CARDS.length - 1);
    added++;
  }}
  if (added > 0) sortOrderAlphabetically();
  return added;
}}

function processImport(text, groupName) {{
  if (!text) return 0;
  const cards = detectAndParse(text);
  if (cards.length === 0) return 0;
  return addCardsToPool(cards, groupName);
}}

async function importFiles(files, groupName) {{
  let total = 0;
  for (const file of files) {{
    const text = await file.text();
    total += processImport(text, groupName);
  }}
  return total;
}}

function showToast(msg) {{
  let toast = document.getElementById('toast');
  if (!toast) {{
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1a1230;border:1px solid #a78bfa;color:#c4b5fd;padding:12px 24px;border-radius:12px;font-size:14px;z-index:200;transition:all 0.3s;opacity:0;pointer-events:none;';
    document.body.appendChild(toast);
  }}
  toast.textContent = msg;
  toast.style.opacity = '1';
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {{ toast.style.opacity = '0'; }}, 2500);
}}

async function doImport() {{
  try {{
    const groupName = document.getElementById('importGroupName').value.trim();
    if (!groupName) {{
      showToast('请填写分组名');
      return;
    }}
    const textareaText = document.getElementById('importTextarea').value.trim();
    const files = document.getElementById('importFileInput').files;

    let added = processImport(textareaText, groupName);
    if (files.length > 0) {{
      added += await importFiles(files, groupName);
    }}

    if (added > 0) {{
      saveCustom();
      // alphaSortAll() already saved cet6-shuffled via sortOrderAlphabetically()
      if (!activeGroup || !getGroups().includes(activeGroup)) {{
        activeGroup = groupName;
      }}
      buildGroupTabs();
      index = 0; flipped = false;
      card.classList.remove('flipped');
      renderCard();
      showToast('成功导入 ' + added + ' 个单词到「' + groupName + '」');
    }} else {{
      showToast('没有新单词被导入（可能已存在或格式不正确）');
    }}
    hideImportModal();
  }} catch(e) {{
    console.error('doImport error:', e);
    showToast('导入失败: ' + e.message);
    hideImportModal();
  }}
}}

// ── Delete group ──
function deleteGroup(groupName) {{
  // Preserve slain status for cards NOT in the deleted group (keyed by word+group)
  const slainKeys = new Set();
  for (const si of slain) {{
    if (si < CARDS.length && CARDS[si].group !== groupName) {{
      slainKeys.add(CARDS[si].word.toLowerCase() + ':::' + CARDS[si].group);
    }}
  }}
  customWords = customWords.filter(c => c.group !== groupName);
  CARDS = CARDS.filter(c => c.group !== groupName);
  // Rebuild slain with correct new indices
  slain.clear();
  for (let i = 0; i < CARDS.length; i++) {{
    if (slainKeys.has(CARDS[i].word.toLowerCase() + ':::' + CARDS[i].group)) {{
      slain.add(i);
    }}
  }}
  saveCustom();
  saveSlain();
  // Rebuild full sequence and save
  alphaSortAll();
  index = 0;
  flipped = false;
  card.classList.remove('flipped');
  activeGroup = null;
  slainChecked.clear();
  buildGroupTabs();
  renderCard();
}}

// ── Reset ──
function showResetModal() {{
  document.getElementById('resetModal').classList.add('show');
}}
function hideResetModal() {{
  document.getElementById('resetModal').classList.remove('show');
}}
function resetAll() {{
  localStorage.removeItem('cet6-slain');
  localStorage.removeItem('cet6-custom');
  localStorage.removeItem('cet6-shuffled');
  localStorage.removeItem('cet6-index');
  location.reload();
}}

// ── Theme toggle ──
const THEME_KEY = 'cet6-theme';
function applyTheme(theme) {{
  if (theme === 'light') {{
    document.body.classList.add('light');
  }} else {{
    document.body.classList.remove('light');
  }}
  updateThemeBtn();
}}
function toggleTheme() {{
  const isLight = document.body.classList.contains('light');
  const next = isLight ? 'dark' : 'light';
  applyTheme(next);
  localStorage.setItem(THEME_KEY, next);
}}
function updateThemeBtn() {{
  const btn = document.getElementById('themeBtn');
  if (!btn) return;
  const isLight = document.body.classList.contains('light');
  btn.textContent = isLight ? '暗色' : '亮色';
}}

// ── Event bindings ──
card.addEventListener('click', flip);

document.addEventListener('keydown', e => {{
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  switch (e.key) {{
    case ' ': e.preventDefault(); flip(); break;
    case 'ArrowLeft': e.preventDefault(); prev(); break;
    case 'ArrowRight': e.preventDefault(); next(); break;
    case 'Escape': flipped && flip(); break;
    case 'r': resetOrder(); break;
    case 'k': slayWord(); break;
  }}
}});

document.getElementById('prevBtn').addEventListener('click', prev);
document.getElementById('nextBtn').addEventListener('click', next);
document.getElementById('flipBtn').addEventListener('click', flip);
document.getElementById('slayBtn').addEventListener('click', slayWord);

document.getElementById('toggleSidebar').addEventListener('click', () => sidebar.classList.toggle('hidden'));
document.getElementById('shuffleBtn').addEventListener('click', shuffleOrder);
document.getElementById('resetOrderBtn').addEventListener('click', resetOrder);
document.getElementById('restoreAllBtn').addEventListener('click', restoreAll);
document.getElementById('emptyImportBtn').addEventListener('click', showImportModal);
document.getElementById('restoreSelectedBtn').addEventListener('click', restoreSelected);
document.getElementById('selectAllSlain').addEventListener('click', selectAllVisibleSlain);
document.getElementById('deselectAllSlain').addEventListener('click', deselectAllSlain);

document.getElementById('resetAllBtn').addEventListener('click', showResetModal);
document.getElementById('deleteGroupBtn').addEventListener('click', () => deleteGroup(activeGroup));
document.getElementById('cancelResetBtn').addEventListener('click', hideResetModal);
document.getElementById('confirmResetBtn').addEventListener('click', resetAll);
document.getElementById('resetModal').addEventListener('click', e => {{ if (e.target.id === 'resetModal') hideResetModal(); }});

document.getElementById('importBtn').addEventListener('click', showImportModal);
document.getElementById('cancelImportBtn').addEventListener('click', hideImportModal);
document.getElementById('confirmImportBtn').addEventListener('click', doImport);
document.getElementById('importModal').addEventListener('click', e => {{ if (e.target.id === 'importModal') hideImportModal(); }});

document.getElementById('themeBtn').addEventListener('click', toggleTheme);

// ── Drag-to-select for batch restore ──
let dragState = null;

// Prevent browser text selection during drag
wordList.addEventListener('selectstart', e => {{
  if (dragState && dragState.dragging) e.preventDefault();
}});

wordList.addEventListener('mousedown', e => {{
  const item = e.target.closest('.word-item');
  if (!item) return;
  const ci = parseInt(item.dataset.cardIdx);
  dragState = {{ startCi: ci, startY: e.clientY, dragging: false, lastCi: ci }};
}});

wordList.addEventListener('mousemove', e => {{
  if (!dragState) return;
  if (!dragState.dragging && Math.abs(e.clientY - dragState.startY) < 5) return;
  dragState.dragging = true;
  e.preventDefault();

  const el = document.elementFromPoint(e.clientX, e.clientY);
  const item = el ? el.closest('.word-item') : null;
  if (!item) return;
  const ci = parseInt(item.dataset.cardIdx);
  if (ci === dragState.lastCi) return;

  // Compute range and direction
  const from = Math.min(dragState.startCi, ci);
  const to = Math.max(dragState.startCi, ci);
  const movingDown = ci >= dragState.startCi;

  // Direct DOM manipulation — no full list rebuild on every move
  wordList.querySelectorAll('.word-item.drag-hover').forEach(el => el.classList.remove('drag-hover'));

  for (let i = from; i <= to; i++) {{
    if (!slain.has(i)) continue;
    const itemEl = wordList.querySelector(`.word-item[data-card-idx="${{i}}"]`);
    if (!itemEl) continue;
    itemEl.classList.add('drag-hover');
    const cb = itemEl.querySelector('.slain-cb');
    if (movingDown) {{
      slainChecked.add(i);
      if (cb) {{ cb.classList.add('checked'); cb.textContent = '\\u2713'; }}
    }} else {{
      slainChecked.delete(i);
      if (cb) {{ cb.classList.remove('checked'); cb.textContent = ''; }}
    }}
  }}
  dragState.lastCi = ci;
  updateBatchRestoreBar();
}});

document.addEventListener('mouseup', () => {{
  if (dragState && dragState.dragging) {{
    wordList.querySelectorAll('.word-item').forEach(el => el.classList.remove('drag-hover'));
    buildWordList(searchBox.value);
    updateBatchRestoreBar();
  }}
  dragState = null;
}});

// Sidebar click handler
wordList.addEventListener('click', e => {{
  if (dragState && dragState.dragging) return;
  const cb = e.target.closest('.slain-cb');
  if (cb) {{
    e.stopPropagation();
    const ci = parseInt(cb.dataset.cb);
    toggleSlainCheck(ci);
    return;
  }}
  const item = e.target.closest('.word-item');
  if (!item) return;
  const ci = parseInt(item.dataset.cardIdx);
  const oi = parseInt(item.dataset.orderIdx);
  if (slain.has(ci)) {{
    restoreWord(ci);
  }} else if (oi >= 0) {{
    goTo(oi);
  }}
}});

// Group tabs click handler
groupTabsCol.addEventListener('click', e => {{
  const tab = e.target.closest('.group-tab-v');
  if (!tab) return;
  filterByGroup(tab.dataset.group);
}});

searchBox.addEventListener('input', e => buildWordList(e.target.value));

// ── Init ──
// Apply saved theme
(function() {{
  const saved = localStorage.getItem(THEME_KEY) || 'dark';
  applyTheme(saved);
}})();

buildGroupTabs();
checkEmpty();
if (getGroupOrder().length > 0) renderCard();
else {{ updateCounts(); buildWordList(); }}
</script>
</body>
</html>
"""

# ── Write output ──
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ 生成完成: {HTML_PATH}")
print(f"   单词数: {total}")
print(f"   大小: {os.path.getsize(HTML_PATH) / 1024 / 1024:.1f} MB")

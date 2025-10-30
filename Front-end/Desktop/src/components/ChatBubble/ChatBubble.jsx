import React, { useEffect, useRef } from "react";
import { getCurrentWindow} from "@tauri-apps/api/window";
import "./styles.css";

export default function ChatBubble() {
  const bubbleRef = useRef(null);

  useEffect(() => {
    const win = getCurrentWindow();
    // arrasto com JS
    const el = bubbleRef.current;
    if (!el) return;
    const onDown = (e) => { e.preventDefault(); win.startDragging().catch(()=>{}); };
    const onDbl = (e) => { e.preventDefault(); e.stopPropagation(); };
    win.isMaximized().then((m) => m && win.unmaximize());

    el.addEventListener("mousedown", onDown, { passive:false });
    el.addEventListener("touchstart", onDown, { passive:false });
    el.addEventListener("dblclick", onDbl, { passive:false });

    return () => {
      el.removeEventListener("mousedown", onDown);
      el.removeEventListener("touchstart", onDown);
      el.removeEventListener("dblclick", onDbl);
    };
  }, []);

  return (
    <div className="cb-root">
      <div ref={bubbleRef} className="cb-bubble">
        <img className="cb-icon" src="src/assets/bubble-icon.png"/>
      </div>
    </div>
  );
}

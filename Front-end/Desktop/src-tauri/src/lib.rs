use tauri::{Manager};
#[tauri::command]

fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![greet])
        .setup(|app| {
            // Obtém a janela 'bubble'
            let window = app.get_webview_window("bubble").unwrap();
            // Força o tamanho para 120x90 (em pixels físicos)
            window.set_size(tauri::Size::Physical(tauri::PhysicalSize::new(80, 80))).unwrap();
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

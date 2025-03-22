pub mod components;
pub mod helpers;
pub mod model;
pub mod router;
pub mod views;

fn main() {
    wasm_logger::init(wasm_logger::Config::default());
    yew::Renderer::<crate::components::app::App>::new().render();
}

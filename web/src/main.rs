use crate::components::app::App;
use yew::Renderer;

pub mod components;
pub mod model;
pub mod router;
pub mod views;

fn main() {
    Renderer::<App>::new().render();
}

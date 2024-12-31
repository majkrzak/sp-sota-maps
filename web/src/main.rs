use crate::components::app::App;
use yew::Renderer;

pub mod components;
pub mod model;
pub mod router;

fn main() {
    Renderer::<App>::new().render();
}

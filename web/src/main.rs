use crate::components::app::App;
use yew::Renderer;

pub mod components;
pub mod model;

fn main() {
    Renderer::<App>::new().render();
}

use yew::{function_component, html, Html};

#[function_component(NotFound)]
pub fn component() -> Html {
    html! {
        <>
          {"404"}
        </>
    }
}

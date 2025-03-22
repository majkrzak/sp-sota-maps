use yew::{html, Html};

pub fn error(err: &anyhow::Error) -> Html {
    html! { <pre>{ format!{"{err:?}"} }</pre> }
}

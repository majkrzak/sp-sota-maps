use yew::{html, Html};
use yew_router::Routable;

use crate::{
    components::{
        about::About, not_found::NotFound, summit_details::SummitDetails, summits::Summits,
    },
    model::reference::Reference,
};

#[derive(Clone, Routable, PartialEq)]
pub enum Route {
    #[at("/")]
    About,
    #[at("/summits")]
    Summits,
    #[at("/*reference")]
    Summit { reference: Reference },
    #[not_found]
    #[at("/404")]
    NotFound,
}

pub fn render(route: Route) -> Html {
    match route {
        Route::About => html! { <About/> },
        Route::Summits => html! { <Summits/> },
        Route::Summit { reference } => {
            html! { <SummitDetails {reference} /> }
        }
        Route::NotFound => html! { <NotFound/> },
    }
}

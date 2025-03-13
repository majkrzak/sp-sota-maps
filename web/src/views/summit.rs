use yew::{html, Html};
use yew_router::prelude::Link;

use crate::{model::summit::Summit, router::Route};

pub fn summit_brief(summit: &Summit) -> Html {
    html! {
        <p>
            <Link<Route> to={Route::Summit{reference:summit.reference.clone()}}>
                { summit.reference.full() }
                { ", " }
                { summit.name.clone() }
                { " – " }
                { format!("{:0.0}m",summit.alt) }
            </Link<Route>>
        </p>
    }
}

use yew::{function_component, html, Html};
use yew_router::{prelude::Link, HashRouter, Routable, Switch};

use crate::{
    components::{about::About, not_found::NotFound, summit::Summit, summits::Summits},
    model::reference::Reference,
};

#[derive(Clone, Routable, PartialEq)]
enum Route {
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

#[function_component(App)]
pub fn component() -> Html {
    html! {
        <>
            <HashRouter>
                <header>
                    <nav>
                        <Link<Route> to={Route::About}>{ "About" }</Link<Route>>
                        <Link<Route> to={Route::Summits}>{ "About" }</Link<Route>>
                        <a href="https://github.com/majkrzak/sp-sota-maps">{"GitHub"}</a>
                        <h1>{"SP SOTA MAPS"}</h1>
                    </nav>
                </header>
                <main>
                    <Switch<Route> render={
                        |route|{
                            match route{
                                Route::About => html! { <About/> },
                                Route::Summits => html! { <Summits/> },
                                Route::Summit{reference} => html! { <Summit {reference} /> },
                                Route::NotFound => html! { <NotFound/> },
                            }
                        }
                    } />
                </main>
                <footer>
                    <p>{"SP-SOTA-MAPS © 2024 Piotr Majkrzak"}</p>
                </footer>
            </HashRouter>
        </>
    }
}

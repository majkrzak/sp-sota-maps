use yew::{function_component, html, Html, Suspense};
use yew_router::{prelude::Link, HashRouter, Switch};

use crate::router::{render, Route};

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
                    <Suspense>
                        <Switch<Route> {render}/>
                    </Suspense>
                </main>
                <footer>
                    <p>{"SP-SOTA-MAPS © 2024 Piotr Majkrzak"}</p>
                </footer>
            </HashRouter>
        </>
    }
}

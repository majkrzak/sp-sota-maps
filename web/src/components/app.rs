use yew::{function_component, html, Html};

#[function_component(App)]
pub fn component() -> Html {
    html! {
        <>
            <header>
                <nav>
                    <a href="#">{"Home"}</a>
                    <a href="#downloads">{"Downloads"}</a>
                    <a href="https://github.com/majkrzak/sp-sota-maps">{"GitHub"}</a>
                    <h1>{"SP SOTA MAPS"}</h1>
                </nav>
            </header>
            <main>
                <img src="https://raw.githubusercontent.com/majkrzak/sp-sota-maps/refs/heads/master/example.png"/>
            </main>
            <footer>
                <p>{"SP-SOTA-MAPS © 2024 Piotr Majkrzak"}</p>
            </footer>
        </>
    }
}

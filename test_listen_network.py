from playwright.sync_api import Page, Route, expect


def test_listen_network(page: Page):
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    page.goto('https://osinit.ru/')


def test_network(page):
    page.route("**/register", lambda route: route.continue_(post_data='{"email": "user","password": "secret"}'))
    page.goto('https://reqres.in/')
    page.get_by_text(' Register - successful ').click()


def test_mock_tags(page):
    page.route("**/api/tags", lambda route: route.fulfill(path="data.json"))
    page.goto('https://demo.realworld.io/')


def test_intercepted(page: Page):
    def handle_route(route: Route):
        response = route.fetch()
        json = response.json()
        json["tags"] = ["open", "solutions"]
        route.fulfill(json=json)

    page.route("**/api/tags", handle_route)

    page.goto("https://demo.realworld.io/")
    sidebar = page.locator('css=div.sidebar') 
    expect(sidebar.get_by_role('link')).to_contain_text(["open", "solutions"])


def test_replace_from_har(page):
    page.goto("https://reqres.in/")
    page.route_from_har("example.har")
    users_single = page.locator('li[data-id="users-single"]')
    users_single.click()
    response = page.locator('[data-key="output-response"]')
    expect(response).to_contain_text("michael.zotov")
    
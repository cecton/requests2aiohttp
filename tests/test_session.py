import aiohttp.test_utils
import requests.sessions
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

import requests2aiohttp.sessions


class Session(requests2aiohttp.sessions.Session, requests.sessions.Session):
    pass


class _TestClient(aiohttp.test_utils.TestClient):
    def __init__(self, server, *, cookie_jar=None, loop=None, **kwargs):
        self._server = server
        self._loop = loop
        if cookie_jar is None:
            cookie_jar = aiohttp.CookieJar(unsafe=True, loop=loop)
        self._session = Session(loop=loop,
                                cookie_jar=cookie_jar,
                                **kwargs)
        self._closed = False
        self._responses = []
        self._websockets = []


class SessionTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.router.add_route('*', '/', lambda x: web.Response(text=x.method))
        app.router.add_route('*', '/error', lambda x: web.Response(status=400))
        app.router.add_route('*', '/json', lambda x: web.json_response(data={}))
        return app

    async def get_client(self, server):
        return _TestClient(server, loop=self.loop)

    @unittest_run_loop
    async def test_get(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.get("/")
        self.assertEqual(await resp.text, "GET")

    @unittest_run_loop
    async def test_options(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.options("/")
        self.assertEqual(await resp.text, "OPTIONS")

    @unittest_run_loop
    async def test_head(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.head("/")
        self.assertEqual(await resp.status_code, 200)

    @unittest_run_loop
    async def test_post(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.post("/")
        self.assertEqual(await resp.text, "POST")

    @unittest_run_loop
    async def test_put(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.put("/")
        self.assertEqual(await resp.text, "PUT")

    @unittest_run_loop
    async def test_patch(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.patch("/")
        self.assertEqual(await resp.text, "PATCH")

    @unittest_run_loop
    async def test_delete(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.delete("/")
        self.assertEqual(await resp.text, "DELETE")

    @unittest_run_loop
    async def test_get(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.request("GET", "/")
        self.assertEqual(await resp.status_code, 200)
        self.assertEqual(await resp.text, "GET")

    @unittest_run_loop
    async def test_invalid_arguments(self):
        self.assertIsInstance(self.client.session, Session)
        with self.assertRaises(RuntimeError):
            await self.client.get("/", stream=True, hooks=None, verify=False)

    @unittest_run_loop
    async def test_raise_for_status(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.request("GET", "/error")
        self.assertEqual(await resp.status_code, 400)
        with self.assertRaises(aiohttp.client_exceptions.ClientResponseError):
            await resp.raise_for_status()
        self.assertEqual(await resp.text, "")

    @unittest_run_loop
    async def test_json(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.request("GET", "/json")
        self.assertEqual(await resp.json(), {})

    @unittest_run_loop
    async def test_bytes(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.request("GET", "/")
        self.assertEqual(await resp.content, b"GET")

    @unittest_run_loop
    async def test_raw(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.request("GET", "/")
        self.assertIsInstance(await resp.raw, aiohttp.client.ClientResponse)

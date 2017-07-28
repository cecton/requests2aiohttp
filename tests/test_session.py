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
        return app

    async def get_client(self, server):
        return _TestClient(server, loop=self.loop)

    @unittest_run_loop
    async def test_get(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.get("/")
        self.assertEqual(await resp.text(), "GET")

    @unittest_run_loop
    async def test_options(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.options("/")
        self.assertEqual(await resp.text(), "OPTIONS")

    @unittest_run_loop
    async def test_head(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.head("/")
        self.assertEqual(resp.status, 200)

    @unittest_run_loop
    async def test_post(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.post("/")
        self.assertEqual(await resp.text(), "POST")

    @unittest_run_loop
    async def test_put(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.put("/")
        self.assertEqual(await resp.text(), "PUT")

    @unittest_run_loop
    async def test_patch(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.patch("/")
        self.assertEqual(await resp.text(), "PATCH")

    @unittest_run_loop
    async def test_delete(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.delete("/")
        self.assertEqual(await resp.text(), "DELETE")

    @unittest_run_loop
    async def test_request(self):
        self.assertIsInstance(self.client.session, Session)
        resp = await self.client.request("GET", "/")
        self.assertEqual(await resp.text(), "GET")

    @unittest_run_loop
    async def test_invalid_arguments(self):
        self.assertIsInstance(self.client.session, Session)
        with self.assertRaises(RuntimeError):
            await self.client.get("/", stream=True, hooks=None, verify=False)

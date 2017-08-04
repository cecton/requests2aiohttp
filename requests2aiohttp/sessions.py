import aiohttp
import asyncio


async def default_exception_wrapper(exc, response):
    return exc


class Session:
    """
    This class needs to be inserted just before the class you intend to inherit
    """

    def __init__(self, **kwargs):
        aio_kwargs, other_kwargs = self._extract_arguments(kwargs)
        self.session = aiohttp.ClientSession(**aio_kwargs)
        super().__init__(**other_kwargs)

    def _extract_arguments(self, kwargs):
        aio_kwargs = {
            k[4:]: v
            for k, v in kwargs.items()
            if k.startswith("aio_")
        }
        rest_kwargs = {
            k: v
            for k, v in kwargs.items()
            if not k.startswith("aio_")
        }
        return (aio_kwargs, rest_kwargs)

    def request(self, method, url, **kwargs):
        return Response(self.session.request(method, url, **kwargs))

    async def close(self):
        await self.session.close()
        super().close()

    def mount(self, prefix, adapter):
        pass

    def prepare_request(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def resolve_redirects(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def rebuild_auth(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def rebuild_method(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def send(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def merge_environment_settings(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def rebuild_proxies(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def get_redirect_target(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def get_adapter(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def __enter__(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def __exit__(self, *args, **kwargs):
        raise RuntimeError("Method not available")  # pragma no cover

    def __getstate__(self):
        raise RuntimeError("Method not available")  # pragma no cover

    def __setstate__(self, state):
        raise RuntimeError("Method not available")  # pragma no cover

    @property
    def __attrs__(self):
        raise RuntimeError("Method not available")  # pragma no cover


class Response:
    """
    _RequestContextManager wrapper for requests.Response compatibility
    """
    def __init__(self, context):
        self.context = context
        self._raise_for_status = None

    @property
    async def response(self):
        if not hasattr(self, '_response'):
            self._response = await self.context
        return self._response

    def raise_for_status(self, wrapper=default_exception_wrapper):
        self._raise_for_status = wrapper

    @property
    def status_code(self):
        return StatusCode(self.response)

    @property
    async def text(self):
        resp = await self.response
        if self._raise_for_status:
            try:
                resp.raise_for_status()
            except Exception as exc:
                raise await self._raise_for_status(exc, resp)
        return await resp.text()

    async def json(self):
        resp = await self.response
        if self._raise_for_status:
            try:
                resp.raise_for_status()
            except Exception as exc:
                raise await self._raise_for_status(exc, resp)
        return await resp.json()

    @property
    async def content(self):
        resp = await self.response
        if self._raise_for_status:
            try:
                resp.raise_for_status()
            except Exception as exc:
                raise await self._raise_for_status(exc, resp)
        return await resp.read()

    @property
    async def raw(self):
        resp = await self.response
        if self._raise_for_status:
            try:
                resp.raise_for_status()
            except Exception as exc:
                raise await self._raise_for_status(exc, resp)
        return resp

    @asyncio.coroutine
    def __iter__(self):
        return self

    def close(self):
        self.context.close()


class StatusCode:
    """
    int wrapper that returns a coroutine with the expected result of the
    boolean expression
    """
    def __init__(self, response):
        self.response = response

    async def __eq__(self, value):
        return (await self.response).status == value

    async def __ne__(self, value):
        return (await self.response).status != value

    async def __lt__(self, value):
        return (await self.response).status < value

    async def __le__(self, value):
        return (await self.response).status <= value

    async def __gt__(self, value):
        return (await self.response).status > value

    async def __ge__(self, value):
        return (await self.response).status >= value

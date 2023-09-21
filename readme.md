# 用法

## casdoor

casdoor是一个CAS认证，[介绍链接🔗](https://casdoor.org/zh/)

## Gradio

[介绍链接🔗](https://www.gradio.app/docs/interface)

# 用途

gradio有自己的登录界面与需求，但是只是简单认证

```python
def same_auth(username, password):
    return username == password
demo.launch(auth=same_auth)
```

Oatuh认证是一个认证功能，只能在huagging face中使用。

```python
import gradio as gr


def hello(profile: gr.OAuthProfile | None) -> str:
    if profile is None:
        return "I don't know you."
    return f"Hello {profile.name}"


with gr.Blocks() as demo:
    gr.LoginButton()
    gr.LogoutButton()
    gr.Markdown().attach_load_event(hello, None)
```

这里就有需要就是希望通过login username password进入界面，那就是需要通过Oauth进行第三方认证。

这里选择`casdoor` 启动服务使用docker进行启动，利用`-d`命令使其不停止一直挂在挂载。

# 代码

想要与casdoor交互，首先要设置这些变量，具体含义查看casdoor文档📄

```python
endpoint = 'http://ip:8000'
client_id = ''
client_secret = ''
certificate = b'''-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----'''
org_name = 'built-in'
states = "test"
scope = "read"
redirect_uri = "http://ip:8000/callback"
```

之后就是要构造`casdoorSDK` 与`url`

```python
sdk = CasdoorSDK(
        endpoint,
        client_id,
        client_secret,
        certificate = certificate,
        org_name = org_name,
        application_name='test'
    )
auth_url = f"{endpoint}/login/oauth/authorize?client_id={client_id}&response_type=code" \
               f"&redirect_uri={redirect_uri}" \
               f"&scope=read&state={states}"
```

之后利用request去访问`auth_url` 然后将获取的内容进行解析

```python
# 获取重定向后的 URL
    redirected_url = responses.url

    # 解析 URL 获取 code 和 state
    parsed_url = urlparse(redirected_url)
    query_params = parse_qs(parsed_url.query)
    code = query_params.get('code')
    state = query_params.get('state')
    print(state)
    print(code)

    # 使用 code 获取访问令牌
    # 使用 await 关键字来等待协程的执行
    token = sdk.get_oauth_token(code=code)
    print(token)
    # 提取访问令牌
    access_token = token.get("access_token")
    username_to_check = usesrname
    user = sdk.get_user(username_to_check)
    if user is not None:
        return True
    else:
        return False
```

具体过程参看[文档📄](https://github.com/casdoor/casdoor-python-sdk)


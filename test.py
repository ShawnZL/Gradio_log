from typing import Optional
import requests
import gradio as gr
from casdoor import CasdoorSDK
from urllib.parse import urlparse, parse_qs

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

def get(usesrname, password):
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

    responses = requests.get(auth_url)

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
def auth_me(username, password):
    from casdoor import CasdoorSDK

    # 创建 CasdoorSDK 实例
    sdk = CasdoorSDK(
        endpoint="https://your-casdoor-endpoint.com",
        client_id="your-client-id",
        client_secret="your-client-secret",
        certificate="your-certificate",  # 证书字符串
        org_name="your-org-name",
        application_name="your-app-name"
    )

    # 要检查的用户名
    username_to_check = "user123"

    # 使用 get_user 方法获取用户信息
    user = sdk.get_user(username_to_check)

    if user is not None:
        print(f"用户 {username_to_check} 存在。")
    else:
        print(f"用户 {username_to_check} 不存在。")

    return False


with gr.Blocks() as demo:
    # 出错提示框
    error_box = gr.Textbox(label="Error", visible=False)
    # 输入框
    name_box = gr.Textbox(label="Name")
    age_box = gr.Number(label="Age")
    symptoms_box = gr.CheckboxGroup(["Cough", "Fever", "Runny Nose"])
    submit_btn = gr.Button("Submit")
    # 输出不可见
    with gr.Column(visible=False) as output_col:
        diagnosis_box = gr.Textbox(label="Diagnosis")
        patient_summary_box = gr.Textbox(label="Patient Summary")
    def submit(name, age, symptoms):
        if len(name) == 0:
            return {error_box: gr.update(value="Enter name", visible=True)}
        if age < 0 or age > 200:
            return {error_box: gr.update(value="Enter valid age", visible=True)}
        return {
            output_col: gr.update(visible=True),
            diagnosis_box: "covid" if "Cough" in symptoms else "flu",
            patient_summary_box: f"{name}, {age} y/o"
        }
    submit_btn.click(
        submit,
        [name_box, age_box, symptoms_box],
        [error_box, diagnosis_box, patient_summary_box, output_col],
    )
demo.launch(auth=get, server_name="0.0.0.0", server_port=8080)



import flet as ft
import requests
import json

def  main(page: ft.Page):
    page.title = "FletPyRequests"
    http_methods = ["GET", "PUT", "DELETE", "PATCH", "POST"]
    method = ft.Dropdown(
        label = "Method",
        width = 130,
        value = "GET",
        options = [ft.dropdown.Option(key=m, text=m) for m in http_methods],
    )
    payload = ft.TextField(label="Enter Payload (JSON)", expand=True, multiline=True)
    url = ft.TextField(label="Enter API URL", expand=True)
    response_text = ft.Text(value="")
    response_status = ft.Text(value="")
    
    
    def send_request(e):
        try:
            request_options = {
                "method": method.value,
                "url": "https://jsonplaceholder.typicode.com/posts/1",
                # "url": url.value,
                "timeout": 10,
                "allow_redirects": False
            }
            if method.value in ["POST", "PUT", "PATCH"] and payload.value.strip():
                try:
                    request_options["json"] = json.loads(payload.value)
                except json.JSONDecodeError as ex:
                    response_text.value = f"Invalid JSON in payload for {method.value} method: {ex}"
                    response_status.value = "Invalid Request Body"
                    response_status.color = ft.Colors.RED
                    return
                
            response = requests.request(**request_options)
            try:
                response_text.value = json.dumps(response.json(), indent=4)
            except requests.exceptions.JSONDecodeError:
                response_text.value = response.text

            response_status.value = f"{response.status_code} -- {response.reason}"
            match response.status_code:
                case code if 200 <= code < 300:
                    response_status.color = ft.Colors.GREEN
                case code if 300 <= code < 400:
                    response_status.color = ft.Colors.BLUE
                case code if 400 <= code < 500:
                    response_status.color = ft.Colors.ORANGE
                case code if 500 <= code < 600:
                    response_status.color = ft.Colors.RED
                case _:
                    response_status.color = ft.Colors.GREY
        except Exception as ex:
            response_text.value = f"Error: {str(ex)}"
            response_status.value = "Request failed"
            response_status.color = ft.Colors.RED
        finally:
            page.update()

    page.add(
        ft.Column(
            controls =[
                ft.Row(
                    controls =[
                        method,
                        url,
                    ],
                ),
                ft.Row(
                    controls =[
                        payload,
                        ft.Button("Send Request", on_click=send_request)
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Text("Response Status: "),
                        response_status,
                    ],
                ),
                ft.Column(
                    controls=[
                        ft.Text("Response: "),
                        response_text
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                )
            ],
            expand=True
        )
    )
            
if __name__ == "__main__":
    ft.run(main)
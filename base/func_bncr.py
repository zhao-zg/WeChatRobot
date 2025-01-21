import requests

class Bncr():
    def __init__(self, conf: dict) -> None:
        self.api_url = conf.get("api_url")
        self.converstion_list = {}

    @staticmethod
    def value_check(conf: dict) -> bool:
        if conf and conf.get("api_url"):
            return True
        return False

    def __repr__(self):
        return 'Bncr'

    def get_answer(self, msg: str, wxid: str, **args) -> str:
        self._update_message(wxid, str(msg), "user")
        data = {
            'id': args["msgInfo"].id,
            'type': args["msgInfo"].type,
            'sender': args["msgInfo"].sender,
            'content': args["msgInfo"].content,
            'is_group': args["msgInfo"].from_group(),
            'roomid': args["msgInfo"].roomid,
        }
        response = requests.post(self.api_url, json=data)
        data = response.json()
        answer = data["data"]
        self._update_message(wxid, answer, "assistant")
        return answer

    def _update_message(self, wxid: str, msg: str, role: str) -> None:
        if wxid not in self.converstion_list.keys():
            self.converstion_list[wxid] = []
        content = {"role": role, "content": str(msg)}
        self.converstion_list[wxid].append(content)


if __name__ == "__main__":
    from configuration import Config
    config = Config().BNCR
    if not config:
        exit(0)

    Bncr = Bncr(config)
    rsp = Bncr.get_answer("你好")
    print(rsp)

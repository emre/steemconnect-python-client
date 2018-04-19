import json


class CustomJsonMixin:

    def get_base_op_structure(self, required_auths, required_posting_auths,
                              custom_operation_id, structure):
        return [
            "custom_json", {
                "required_auths": required_auths,
                "required_posting_auths": required_posting_auths,
                "id": custom_operation_id,
                "json": json.dumps(structure),
            }
        ]

import os, argparse, importlib, yaml
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# Map tên resource -> module.Class
AVAILABLE = {
    "User": "models.user_schema.UserSchema",
    "Product": "models.product_schema.ProductSchema",
    "Order": "models.order_schema.OrderSchema",
}

def import_class(path):
    module_name, class_name = path.rsplit(".", 1)
    mod = importlib.import_module(module_name)
    return getattr(mod, class_name)

def generate_crud_for(spec, resource_name, SchemaClass):
    # register schema and input schema (exclude id)
    spec.components.schema(resource_name, schema=SchemaClass())
    class InputSchema(SchemaClass):
        class Meta:
            exclude = ("id",)
    spec.components.schema(f"{resource_name}Input", schema=InputSchema())

    base = f"/{resource_name.lower()}s"
    # GET all + POST
    spec.path(
        path=base,
        operations={
            "get": {
                "summary": f"Lấy tất cả {resource_name}",
                "tags": [resource_name],
                "responses": {
                    "200": {
                        "description": f"Danh sách {resource_name}",
                        "schema": {"type": "array", "items": {"$ref": f"#/definitions/{resource_name}"}},
                    }
                }
            },
            "post": {
                "summary": f"Tạo {resource_name}",
                "tags": [resource_name],
                "parameters": [
                    {"in": "body", "name": "body", "required": True, "schema": {"$ref": f"#/definitions/{resource_name}Input"}}
                ],
                "responses": {"201": {"description": f"{resource_name} đã tạo", "schema": {"$ref": f"#/definitions/{resource_name}"}}}
            }
        }
    )
    # GET/PUT/DELETE by id
    spec.path(
        path=f"{base}" + "/{id}",
        operations={
            "get": {
                "summary": f"Lấy {resource_name} theo ID",
                "tags": [resource_name],
                "parameters": [{"name": "id", "in": "path", "type": "integer", "required": True}],
                "responses": {"200": {"description": resource_name, "schema": {"$ref": f"#/definitions/{resource_name}"}}, "404": {"description": "Not found"}}
            },
            "put": {
                "summary": f"Cập nhật {resource_name}",
                "tags": [resource_name],
                "parameters": [
                    {"name": "id", "in": "path", "type": "integer", "required": True},
                    {"in": "body", "name": "body", "required": True, "schema": {"$ref": f"#/definitions/{resource_name}Input"}}
                ],
                "responses": {"200": {"description": f"{resource_name} updated", "schema": {"$ref": f"#/definitions/{resource_name}"}}, "404": {"description": "Not found"}}
            },
            "delete": {
                "summary": f"Xóa {resource_name}",
                "tags": [resource_name],
                "parameters": [{"name": "id", "in": "path", "type": "integer", "required": True}],
                "responses": {"200": {"description": f"{resource_name} deleted"}, "404": {"description": "Not found"}}
            }
        }
    )

def main(selected=None):
    spec = APISpec(title="Access Backend API", version="1.0.0", openapi_version="2.0",
                   info={"description": "Auto-generated CRUD spec from Marshmallow schemas"},
                   plugins=[MarshmallowPlugin()])

    keys = selected if selected else list(AVAILABLE.keys())
    for k in keys:
        if k not in AVAILABLE:
            print(f"Warning: {k} not in AVAILABLE list, skipping.")
            continue
        cls = import_class(AVAILABLE[k])
        generate_crud_for(spec, k, cls)

    out = os.path.join("swagger", "swagger_generated.yaml")
    os.makedirs("swagger", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        yaml.dump(spec.to_dict(), f, allow_unicode=True)
    print("✅ Generated:", out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--schemas", nargs="*", help="Names of schemas to include (e.g. User Product)")
    args = parser.parse_args()
    main(selected=args.schemas)

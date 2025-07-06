import sys
import json

def main():
    # Read from stdin
    raw_input = sys.stdin.read()
    try:
        data = json.loads(raw_input)
    except Exception as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
        return

    # Extract 'name' if provided
    name = data.get("input", {}).get("name", "world")

    # Respond with static message
    response = {
        "output": {
            "message": f"Hello, {name}!"
        }
    }

    print(json.dumps(response))

if __name__ == "__main__":
    main()

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("\n  MND Wealth Workshop")
    print("  http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000, host='127.0.0.1')

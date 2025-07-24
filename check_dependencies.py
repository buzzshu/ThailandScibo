try:
    import flask
    import matplotlib
    print('Flask和matplotlib已安裝')
except ImportError as e:
    print(f'缺少套件: {e}')

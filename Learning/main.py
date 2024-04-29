try:
    v = 10 / 0
    print('done', v)
except Exception as e:
    import traceback
    traceback.print_exc()
    print(e)

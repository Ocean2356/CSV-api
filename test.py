import client

if __name__ == '__main__':
    print("init")
    cli = client.Client()
    print()

    print("clear")
    cli.do_clear("")
    print()

    print("create")
    cli.do_create("sample_data_1.csv")
    print()

    print("info")
    cli.do_info("sample_data_1.csv")
    print()

    print("list")
    cli.do_list("")
    print()

    print("excel")
    cli.do_excel("sample_data_1.csv")
    print()

    print("stats")
    cli.do_stats("sample_data_1.csv")
    print()

    # BUG in server
    # print("plot")
    # cli.do_plot("sample_data_1.csv")
    # print()

    print("delete")
    cli.do_delete("sample_data_1.csv")
    print()

    print("list")
    cli.do_list("")
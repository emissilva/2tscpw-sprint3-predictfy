#!/usr/bin/env python3
"""Executa SQL no MySQL efêmero usando segredo somente do ambiente."""
import os
import sys
from pathlib import Path

import pymysql

required = ("MYSQL_FQDN", "MYSQL_ADMIN_PASSWORD")
missing = [name for name in required if not os.environ.get(name)]
if missing:
    raise SystemExit(f"Variáveis ausentes: {', '.join(missing)}")

connection = pymysql.connect(
    host=os.environ["MYSQL_FQDN"],
    user=os.environ.get("MYSQL_ADMIN_USER", "predictfyadmin"),
    password=os.environ["MYSQL_ADMIN_PASSWORD"],
    database=os.environ.get("MYSQL_DATABASE", "predictfy"),
    ssl={"check_hostname": True},
    autocommit=True,
)

with connection:
    with connection.cursor() as cursor:
        if len(sys.argv) == 2:
            sql = Path(sys.argv[1]).read_text(encoding="utf-8")
            for statement in (item.strip() for item in sql.split(";")):
                if statement:
                    cursor.execute(statement)
                    if cursor.description:
                        print("\t".join(column[0] for column in cursor.description))
                        for row in cursor.fetchall():
                            print("\t".join(str(value) for value in row))
        else:
            cursor.execute("SELECT VERSION(), DATABASE()")
            print(cursor.fetchone())

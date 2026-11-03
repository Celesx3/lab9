# Lab 9 PDDL

Лабораторийн эхний хэсэг буюу Алхам 1–5: гэрлийн жишээ, Blocksworld domain,
гурван problem, төлөвлөгөөг шалгах тусдаа Python симулятор.

## Ажиллуулах

Python 3.9 буюу түүнээс шинэ хувилбар шаардлагатай. Windows PowerShell дээр
репозиторийн үндсэн хавтсаас:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pyperplan==2.1
.\.venv\Scripts\python.exe run_lab.py
```

`run_lab.py` нь гэрлийн хоёр жишээ, Blocksworld-ийн гурван бодлогыг BFS-ээр
шийдэж, уртыг нь шалгана. Blocksworld-ийн төлөвлөгөөнүүдийг симулятороор
баталж, зориудаар өгсөн хоёр буруу төлөвлөгөөг няцааж байгааг мөн шалгана.

| Бодлого | Хүлээгдсэн үйлдлийн тоо |
| --- | ---: |
| light_problem | 1 |
| light_already_on | 0 |
| p01 | 4 |
| p02 | 6 |
| p03 | 8 |

Гарсан төлөвлөгөөг `pddl/*.soln`, log-уудыг `results/*.txt` дотор хадгална.
Буруу төлөвлөгөөний хоёр жишээг `examples/` хавтсанд ажиллуулах үед үүсгэнэ.
`.soln` болон `.txt` файлуудыг `.gitignore`-оор хассан тул GitHub-д орохгүй.

Нэг бодлогыг тусад нь ажиллуулах:

```powershell
.\.venv\Scripts\python.exe -m pyperplan -s bfs pddl\blocks_domain.pddl pddl\p01.pddl
.\.venv\Scripts\python.exe sim.py pddl\p01.pddl
```

## Кодын бүтэц

- `pddl/` — гэрлийн болон Blocksworld-ийн domain, problem файлууд.
- `sim.py` — төлөвлөгчийн operator-оос үл хамаарах STRIPS симулятор.
- `run_lab.py` — дахин ажиллуулах, үр дүнг шалгах скрипт.

Алхам 6–9 буюу хайлт ба heuristic-ийн харьцуулалт, domain-ы алдааны туршилт,
Logistics бодлогууд нь үлдсэн хэсэг болно.

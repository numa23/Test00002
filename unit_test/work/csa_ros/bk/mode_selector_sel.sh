# target param copy


for index in {2..2}
do
    x="000${index}"
    python3 exec_unit_test.py mode_selector 002 ${x: -3}
done


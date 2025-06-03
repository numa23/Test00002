# target param copy


for index in {1..5}
do
    x="000${index}"
    python3 exec_unit_test2.py mode_selector 006 ${x: -3}
done


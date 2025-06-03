# target param copy


for index in {1..40}
do
    x="000${index}"
    python3 exec_unit_test.py mode_selector 001 ${x: -3}
done



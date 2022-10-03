import main

def test_weekcount():
   assert main.weekcount == [54]

def test_comaverage():
    assert main.comaverage == [746]

def test_comperminus():
   assert main.comperminus == 596

def test_comperplus():
   assert main.comperplus == 895

def test_total_outliers():
   assert main.total_outliers() == 13


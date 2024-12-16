from helper.models import SearchModel

def test_search_model():
    text = "12.根据权利要求3-10任一项所述的场效应晶体管，其特征在于，所述电流引导层（9）的掺杂浓度大于所述外延层，所述电流引导层在下侧。"
    m = SearchModel(r"掺杂浓度|电流")
    result = m.search(text)
    assert result['掺杂浓度'] == [(43, 47)]
    assert result['电流'] == [(34, 36), (57, 59)]
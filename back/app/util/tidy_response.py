import json


def tidy_response(data):
    """
    データを整理し、corporate_number ごとにまとめ、
    同じ要素を統合し、各データ項目にsource URLを含める。
    corporate_number が null の場合は、企業名をキーとする。

    Args:
        data (list): データを含むリスト。

    Returns:
        dict: 加工されたデータを含む辞書。
    """
    processed_data = {}

    for item in data:
        if "response" in item:
            response = item["response"]
            source_url = item.get("source")
            company_name = None
            corporate_number = None
            company_data = {
                "name": {"value": None, "source": None},
                "representatives": {"value": [], "source": None},
                "features": {"value": None, "source": None},
                "phone_number": {"value": None, "source": None},
                "email": {"value": None, "source": None},
                "headquarters_location": {"value": None, "source": None},
                "establishment_year": {"value": None, "source": None},
                "business_activities": {"value": None, "source": None},
                "sales": {},
                "employees": {},
                "offices": {},
                "factories": {},
                "stores": {},
                "net_profit": {},
                "capital": {},
                "company_history": {"value": None, "source": None},
                "philosophy": {"value": None, "source": None},
                "strengths": {"value": [], "source": None},
                "weaknesses": {"value": [], "source": None},
                "opportunities": {"value": [], "source": None},
                "threats": {"value": [], "source": None},
                "competitors": {"value": [], "source": None},
                "businesses": {"value": [], "source": None},
                "human_resources": {
                    "ideal": {"value": None, "source": None},
                    "skills": {"value": [], "source": None},
                },
                "corporate_number": None,
            }

            for entry in response:
                if entry.get("name") == "会社名":
                    company_data["name"]["value"] = entry.get("value")
                    company_data["name"]["source"] = source_url
                    company_name = entry.get("value")
                elif entry.get("name") == "代表者":
                    if entry.get("value"):
                        representatives = [
                            rep.strip() for rep in entry.get("value").split("、")
                        ]
                        company_data["representatives"]["value"].extend(representatives)
                        company_data["representatives"]["source"] = source_url
                elif entry.get("name") == "特色":
                    company_data["features"]["value"] = entry.get("value")
                    company_data["features"]["source"] = source_url
                elif entry.get("name") == "電話番号":
                    company_data["phone_number"]["value"] = (
                        entry.get("value") if entry.get("value") != "非公開" else None
                    )
                    company_data["phone_number"]["source"] = source_url
                elif entry.get("name") == "メールアドレス":
                    company_data["email"]["value"] = (
                        entry.get("value") if entry.get("value") != "非公開" else None
                    )
                    company_data["email"]["source"] = source_url
                elif entry.get("name") == "本社所在地":
                    company_data["headquarters_location"]["value"] = entry.get("value")
                    company_data["headquarters_location"]["source"] = source_url
                elif entry.get("name") == "設立年":
                    company_data["establishment_year"]["value"] = entry.get("value")
                    company_data["establishment_year"]["source"] = source_url
                elif entry.get("name") == "事業内容":
                    company_data["business_activities"]["value"] = entry.get("value")
                    company_data["business_activities"]["source"] = source_url
                elif entry.get("name") == "売上高":
                    if entry["year"] and entry.get("value") is not None:
                        company_data["sales"][entry["year"]] = {
                            "value": entry.get("value"),
                            "source": source_url,
                        }
                elif entry.get("name") == "従業員数":
                    if entry["year"] and entry.get("value") is not None:
                        company_data["employees"][entry["year"]] = {
                            "value": entry.get("value"),
                            "source": source_url,
                        }
                elif entry.get("name") == "店舗数":
                    if entry["year"] and entry.get("value") is not None:
                        company_data["stores"][entry["year"]] = {
                            "value": entry.get("value"),
                            "source": source_url,
                        }
                elif entry.get("name") == "事業所数":
                    if entry["year"] and entry.get("value") is not None:
                        company_data["offices"][entry["year"]] = {
                            "value": entry.get("value"),
                            "source": source_url,
                        }
                elif entry.get("name") == "工場数":
                    if entry["year"] and entry.get("value") is not None:
                        company_data["factories"][entry["year"]] = {
                            "value": entry.get("value"),
                            "source": source_url,
                        }
                elif entry.get("name") == "当期純利益":
                    if entry["year"] and entry.get("value") is not None:
                        company_data["net_profit"][entry["year"]] = {
                            "value": entry.get("value"),
                            "source": source_url,
                        }
                elif entry.get("name") == "資本金":
                    if entry["year"] and entry.get("value") is not None:
                        company_data["capital"][entry["year"]] = {
                            "value": entry.get("value"),
                            "source": source_url,
                        }
                elif entry.get("name") == "企業の沿革":
                    company_data["company_history"]["value"] = entry.get("value")
                    company_data["company_history"]["source"] = source_url
                elif entry.get("name") == "理念":
                    company_data["philosophy"]["value"] = entry.get("value")
                    company_data["philosophy"]["source"] = source_url
                elif entry.get("name") == "強み":
                    if entry.get("value"):
                        strengths = [
                            s.strip()
                            for s in entry.get("value").replace("\n", "").split("・")
                            if s.strip()
                        ]
                        company_data["strengths"]["value"].extend(strengths)
                        company_data["strengths"]["source"] = source_url
                elif entry.get("name") == "弱み":
                    if entry.get("value"):
                        weaknesses = [
                            s.strip()
                            for s in entry.get("value").replace("\n", "").split("・")
                            if s.strip()
                        ]
                        company_data["weaknesses"]["value"].extend(weaknesses)
                        company_data["weaknesses"]["source"] = source_url
                elif entry.get("name") == "機会":
                    if entry.get("value"):
                        opportunities = [
                            s.strip()
                            for s in entry.get("value").replace("\n", "").split("・")
                            if s.strip()
                        ]
                        company_data["opportunities"]["value"].extend(opportunities)
                        company_data["opportunities"]["source"] = source_url
                elif entry.get("name") == "脅威":
                    if entry.get("value"):
                        threats = [
                            s.strip()
                            for s in entry.get("value").replace("\n", "").split("・")
                            if s.strip()
                        ]
                        company_data["threats"]["value"].extend(threats)
                        company_data["threats"]["source"] = source_url
                elif entry.get("name").startswith("競合企業"):
                    if entry.get("value"):
                        company_data["competitors"]["value"].append(entry.get("value"))
                        company_data["competitors"]["source"] = source_url
                elif entry.get("name").startswith("事業"):
                    if entry.get("value"):
                        company_data["businesses"]["value"].append(entry.get("value"))
                        company_data["businesses"]["source"] = source_url
                elif entry.get("name") == "求める人材像":
                    company_data["human_resources"]["ideal"]["value"] = entry.get(
                        "value"
                    )
                    company_data["human_resources"]["ideal"]["source"] = source_url
                elif entry.get("name").startswith("スキル"):
                    company_data["human_resources"]["skills"]["value"].append(
                        entry.get("value")
                    )
                    company_data["human_resources"]["skills"]["source"] = source_url

            corporate_number = item.get("corporate_number")
            company_data["corporate_number"] = corporate_number

            key = corporate_number if corporate_number else company_name

            if key not in processed_data:
                processed_data[key] = company_data
            else:
                # 既存のデータと新しいデータをマージ
                existing_data = processed_data[key]

                # リストをextendする
                existing_data["representatives"]["value"].extend(
                    company_data["representatives"]["value"]
                )
                existing_data["strengths"]["value"].extend(
                    company_data["strengths"]["value"]
                )
                existing_data["weaknesses"]["value"].extend(
                    company_data["weaknesses"]["value"]
                )
                existing_data["opportunities"]["value"].extend(
                    company_data["opportunities"]["value"]
                )
                existing_data["threats"]["value"].extend(
                    company_data["threats"]["value"]
                )
                existing_data["competitors"]["value"].extend(
                    company_data["competitors"]["value"]
                )
                existing_data["businesses"]["value"].extend(
                    company_data["businesses"]["value"]
                )
                existing_data["human_resources"]["skills"]["value"].extend(
                    company_data["human_resources"]["skills"]["value"]
                )
                # ソース情報をマージ
                if company_data["representatives"]["source"]:
                    existing_data["representatives"]["source"] = company_data[
                        "representatives"
                    ]["source"]
                if company_data["strengths"]["source"]:
                    existing_data["strengths"]["source"] = company_data["strengths"][
                        "source"
                    ]
                if company_data["weaknesses"]["source"]:
                    existing_data["weaknesses"]["source"] = company_data["weaknesses"][
                        "source"
                    ]
                if company_data["opportunities"]["source"]:
                    existing_data["opportunities"]["source"] = company_data[
                        "opportunities"
                    ]["source"]
                if company_data["threats"]["source"]:
                    existing_data["threats"]["source"] = company_data["threats"][
                        "source"
                    ]
                if company_data["competitors"]["source"]:
                    existing_data["competitors"]["source"] = company_data[
                        "competitors"
                    ]["source"]
                if company_data["businesses"]["source"]:
                    existing_data["businesses"]["source"] = company_data["businesses"][
                        "source"
                    ]
                if company_data["human_resources"]["skills"]["source"]:
                    existing_data["human_resources"]["skills"]["source"] = company_data[
                        "human_resources"
                    ]["skills"]["source"]

                # 既存のデータを更新する
                if company_data["name"]["value"]:
                    existing_data["name"]["value"] = company_data["name"]["value"]
                    existing_data["name"]["source"] = company_data["name"]["source"]
                if company_data["features"]["value"]:
                    existing_data["features"]["value"] = company_data["features"][
                        "value"
                    ]
                    existing_data["features"]["source"] = company_data["features"][
                        "source"
                    ]
                if company_data["phone_number"]["value"]:
                    existing_data["phone_number"]["value"] = company_data[
                        "phone_number"
                    ]["value"]
                    existing_data["phone_number"]["source"] = company_data[
                        "phone_number"
                    ]["source"]
                if company_data["email"]["value"]:
                    existing_data["email"]["value"] = company_data["email"]["value"]
                    existing_data["email"]["source"] = company_data["email"]["source"]
                if company_data["headquarters_location"]["value"]:
                    existing_data["headquarters_location"]["value"] = company_data[
                        "headquarters_location"
                    ]["value"]
                    existing_data["headquarters_location"]["source"] = company_data[
                        "headquarters_location"
                    ]["source"]
                if company_data["establishment_year"]["value"]:
                    existing_data["establishment_year"]["value"] = company_data[
                        "establishment_year"
                    ]["value"]
                    existing_data["establishment_year"]["source"] = company_data[
                        "establishment_year"
                    ]["source"]
                if company_data["business_activities"]["value"]:
                    existing_data["business_activities"]["value"] = company_data[
                        "business_activities"
                    ]["value"]
                    existing_data["business_activities"]["source"] = company_data[
                        "business_activities"
                    ]["source"]
                if company_data["company_history"]["value"]:
                    existing_data["company_history"]["value"] = company_data[
                        "company_history"
                    ]["value"]
                    existing_data["company_history"]["source"] = company_data[
                        "company_history"
                    ]["source"]
                if company_data["philosophy"]["value"]:
                    existing_data["philosophy"]["value"] = company_data["philosophy"][
                        "value"
                    ]
                    existing_data["philosophy"]["source"] = company_data["philosophy"][
                        "source"
                    ]
                if company_data["human_resources"]["ideal"]["value"]:
                    existing_data["human_resources"]["ideal"]["value"] = company_data[
                        "human_resources"
                    ]["ideal"]["value"]
                    existing_data["human_resources"]["ideal"]["source"] = company_data[
                        "human_resources"
                    ]["ideal"]["source"]

                # 辞書型の値をupdateする
                existing_data["sales"].update(company_data["sales"])
                existing_data["employees"].update(company_data["employees"])
                existing_data["offices"].update(company_data["offices"])
                existing_data["factories"].update(company_data["factories"])
                existing_data["stores"].update(company_data["stores"])
                existing_data["net_profit"].update(company_data["net_profit"])
                existing_data["capital"].update(company_data["capital"])

                # 重複を削除
                existing_data["representatives"]["value"] = list(
                    set(existing_data["representatives"]["value"])
                )
                existing_data["strengths"]["value"] = list(
                    set(existing_data["strengths"]["value"])
                )
                existing_data["weaknesses"]["value"] = list(
                    set(existing_data["weaknesses"]["value"])
                )
                existing_data["opportunities"]["value"] = list(
                    set(existing_data["opportunities"]["value"])
                )
                existing_data["threats"]["value"] = list(
                    set(existing_data["threats"]["value"])
                )
                existing_data["competitors"]["value"] = list(
                    set(existing_data["competitors"]["value"])
                )
                existing_data["businesses"]["value"] = list(
                    set(existing_data["businesses"]["value"])
                )
                existing_data["human_resources"]["skills"]["value"] = list(
                    set(existing_data["human_resources"]["skills"]["value"])
                )

                processed_data[key] = existing_data  # 更新したデータを格納

    return processed_data


if __name__ == "__main__":
    data = [
        {
            "response": [
                {
                    "name": "会社名",
                    "value": "ソニーグループ株式会社 (Sony Group Corporation)",
                },
                {
                    "name": "代表者",
                    "value": "会長 CEO 吉田 憲一郎、社長 COO 兼 CFO 十時 裕樹",
                },
                {
                    "name": "特色",
                    "value": "ゲーム＆ネットワークサービス、音楽、映画、エレクトロニクス製品など幅広い事業を展開",
                },
                {"name": "電話番号", "value": "03-6748-2111 (代表)"},
                {"name": "メールアドレス", "value": None},
                {"name": "本社所在地", "value": "〒108-0075 東京都港区港南1-7-1"},
                {"name": "設立年", "value": "1946年"},
                {
                    "name": "事業内容",
                    "value": "ゲーム＆ネットワークサービス、音楽、映画、エンタテインメント・テクノロジー＆サービス（モバイル・コミュニケーション/イメージング・プロダクツ＆ソリューション/ホームエンタテインメント＆サウンド）、イメージング＆センシング・ソリューション、金融及びその他の事業",
                },
                {"name": "売上高", "year": "2024", "value": None},
                {"name": "売上高", "year": "2023", "value": "13兆208億円"},
                {"name": "売上高", "year": "2022", "value": None},
                {"name": "従業員数", "year": "2024", "value": "113,000名"},
                {"name": "従業員数", "year": "2023", "value": None},
                {"name": "従業員数", "year": "2022", "value": None},
                {"name": "店舗数", "year": "2024", "value": None},
                {"name": "店舗数", "year": "2023", "value": None},
                {"name": "店舗数", "year": "2022", "value": None},
                {"name": "事業所数", "year": "2024", "value": None},
                {"name": "事業所数", "year": "2023", "value": None},
                {"name": "事業所数", "year": "2022", "value": None},
                {"name": "工場数", "year": "2024", "value": None},
                {"name": "工場数", "year": "2023", "value": None},
                {"name": "工場数", "year": "2022", "value": None},
                {"name": "当期純利益", "year": "2024", "value": None},
                {"name": "当期純利益", "year": "2023", "value": None},
                {"name": "当期純利益", "year": "2022", "value": None},
                {"name": "資本金", "year": "2024", "value": "8,814億円"},
                {"name": "資本金", "year": "2023", "value": None},
                {"name": "資本金", "year": "2022", "value": None},
                {"name": "企業の沿革", "value": "1946年設立"},
                {"name": "理念", "value": None},
            ],
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/data/",
            "corporate_number": None,
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニー株式会社"},
                {"name": "代表者", "value": "槙 公雄"},
                {"name": "特色", "value": "エンタテインメント・テクノロジー&サービス"},
                {"name": "電話番号", "value": None},
                {"name": "メールアドレス", "value": None},
                {"name": "本社所在地", "value": "〒108-0075 東京都港区港南1-7-1"},
                {"name": "設立年", "value": "2021年4月1日"},
                {
                    "name": "事業内容",
                    "value": "エンタテインメント・テクノロジー&サービス（ホームエンタテインメント、パーソナルエンタテインメント、イメージングエンタテインメント、プロフェッショナルイメージングテクノロジー、レンズテクノロジー&システム、メディアソリューション、モバイルコミュニケーションズ、ライフサイエンス&テクノロジー、ソフトウェアサービス、スポーツエンタテインメント、セキュアテクノロジー&ソリューション、VPテクノロジー&サービス、ネットワークサービス、他）",
                },
                {"name": "売上高", "year": "2024", "value": None},
                {"name": "売上高", "year": "2023", "value": None},
                {"name": "売上高", "year": "2022", "value": "2兆4,760億円"},
                {"name": "従業員数", "year": "2024", "value": None},
                {"name": "従業員数", "year": "2023", "value": "約9,000名"},
                {"name": "従業員数", "year": "2022", "value": None},
                {"name": "店舗数", "year": "2024", "value": None},
                {"name": "店舗数", "year": "2023", "value": None},
                {"name": "店舗数", "year": "2022", "value": None},
                {"name": "事業所数", "year": "2024", "value": None},
                {"name": "事業所数", "year": "2023", "value": None},
                {"name": "事業所数", "year": "2022", "value": None},
                {"name": "工場数", "year": "2024", "value": None},
                {"name": "工場数", "year": "2023", "value": None},
                {"name": "工場数", "year": "2022", "value": None},
                {"name": "当期純利益", "year": "2024", "value": None},
                {"name": "当期純利益", "year": "2023", "value": None},
                {"name": "当期純利益", "year": "2022", "value": None},
                {"name": "資本金", "year": "2024", "value": "30億円"},
                {"name": "資本金", "year": "2023", "value": None},
                {"name": "資本金", "year": "2022", "value": None},
                {
                    "name": "企業の沿革",
                    "value": "2021年4月1日付をもって、ソニーエレクトロニクス株式会社、ソニーイメージングプロダクツ&ソリューションズ株式会社、ソニーホームエンタテインメント&サウンドプロダクツ株式会社及びソニーモバイルコミュニケーションズ株式会社の四社を統合し、統合後の会社の社名を「ソニー株式会社」としました。（同日付で、旧・ソニー株式会社は「ソニーグループ株式会社」に社名変更しています。）",
                },
                {"name": "理念", "value": None},
            ],
            "source": "https://www.sony.co.jp/corporate/",
            "corporate_number": None,
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {
                    "name": "特色",
                    "value": "エレクトロニクス、エンタテインメント、金融など幅広い事業を展開するグローバル企業",
                },
                {"name": "電話番号", "value": "非公開"},
                {"name": "メールアドレス", "value": "非公開"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {"name": "設立年", "value": "1946年"},
                {
                    "name": "事業内容",
                    "value": "エレクトロニクス製品の製造販売、ゲーム・ネットワークサービス、音楽・映画制作配給、金融サービスなど",
                },
                {"name": "売上高", "year": "2024", "value": "非公開"},
                {"name": "売上高", "year": "2023", "value": "約10兆円"},
                {"name": "売上高", "year": "2022", "value": "約9兆円"},
                {"name": "従業員数", "year": "2024", "value": "非公開"},
                {"name": "従業員数", "year": "2023", "value": "約11万人"},
                {"name": "従業員数", "year": "2022", "value": "約11万人"},
                {"name": "店舗数", "year": "2024", "value": "非公開"},
                {"name": "店舗数", "year": "2023", "value": "非公開"},
                {"name": "店舗数", "year": "2022", "value": "非公開"},
                {"name": "事業所数", "year": "2024", "value": "非公開"},
                {"name": "事業所数", "year": "2023", "value": "非公開"},
                {"name": "事業所数", "year": "2022", "value": "非公開"},
                {"name": "工場数", "year": "2024", "value": "非公開"},
                {"name": "工場数", "year": "2023", "value": "非公開"},
                {"name": "工場数", "year": "2022", "value": "非公開"},
                {"name": "当期純利益", "year": "2024", "value": "非公開"},
                {"name": "当期純利益", "year": "2023", "value": "約8000億円"},
                {"name": "当期純利益", "year": "2022", "value": "約7000億円"},
                {"name": "資本金", "year": "2024", "value": "非公開"},
                {"name": "資本金", "year": "2023", "value": "非公開"},
                {"name": "資本金", "year": "2022", "value": "非公開"},
                {
                    "name": "企業の沿革",
                    "value": "1946年創業。戦後日本の復興期にラジオの修理から始まり、トランジスタラジオ、ウォークマン、プレイステーションなど、数々の革新的な製品を生み出してきた。",
                },
                {
                    "name": "理念",
                    "value": "クリエイティビティとテクノロジーの力で、世界を感動で満たす。",
                },
            ],
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニー企業株式会社"},
                {"name": "代表者", "value": ""},
                {"name": "本社所在地", "value": ""},
                {
                    "name": "理念",
                    "value": "私たちのミッションは「場」を使った新しいブランドコミュニケーションによりお客様に感動をお届けすることです。このミッションを実現させるためのコンセプトは「3IN」。\n\n* Inviting（招く・誘う・誘惑する）* Inspiring（刺激・感動・鼓舞する）* Interweaving（織り込む・組み合わす・織り成す）\n\n自由でオープンであり、余白・余地・余裕があること。\n好奇心を刺激する、未来、発想、遊び、技術で人々を鼓舞すること。\nモノ・コト・ヒト、複数の価値観が組み合わされていること。\n\n私たちはこれらの3つの考え方を日々の仕事のスタンスや、人々との関わり方に組み入れることで、都市や社会、そして未来を面白くする会社であり続けます。",
                },
            ],
            "source": "https://www.sonykigyo.jp/company/philosophy2.html",
            "corporate_number": None,
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {
                    "name": "理念",
                    "value": "クリエイティビティとテクノロジーの力で、世界を感動で満たす",
                },
            ],
            "source": "https://www.sony.com/ja/SonyInfo/csr/vision/",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニー株式会社"},
                {"name": "代表者", "value": "不明"},
                {"name": "本社所在地", "value": "不明"},
                {
                    "name": "理念",
                    "value": "テクノロジーの力で未来のエンタテインメントをクリエイターと共創する。世界中の人に感動を提供し続ける。",
                },
            ],
            "source": "https://www.sony.co.jp/corporate/mission-vision/",
            "corporate_number": None,
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {
                    "name": "強み",
                    "value": "多様な事業ポートフォリオ、高い技術力、グローバル展開力、強力なブランド力",
                },
                {
                    "name": "弱み",
                    "value": "一部事業の収益性低迷、円高による影響、人材確保競争の激化",
                },
                {
                    "name": "機会",
                    "value": "AI、IoT、5Gなどの技術革新、新興市場の拡大、サステナビリティへの関心の高まり",
                },
                {
                    "name": "脅威",
                    "value": "競合他社の台頭、地政学的リスク、原材料価格の高騰、世界経済の減速",
                },
            ],
            "source": "https://www.sony.com/ja/SonyInfo/DiscoverSony/articles/202402/sgcpr/",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南"},
                {
                    "name": "強み",
                    "value": "・世界シェアトップのイメージセンサー事業\n・多角化された事業ポートフォリオによる安定性\n・高いブランド力と技術力\n・グローバル展開による市場機会の拡大",
                },
                {
                    "name": "弱み",
                    "value": "・特定事業への依存\n・競争激化による収益圧力\n・円高による収益悪化\n・人材確保の難しさ",
                },
                {
                    "name": "機会",
                    "value": "・AI・IoT関連技術の進展\n・EV・自動運転技術の普及\n・新興国市場の成長\n・M&Aによる事業拡大",
                },
                {
                    "name": "脅威",
                    "value": "・競合他社の技術革新\n・世界経済の減速\n・地政学的リスク\n・サプライチェーンの混乱",
                },
            ],
            "source": "https://semi-journal.jp/career/company/sony.html",
            "corporate_number": None,
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {
                    "name": "代表者",
                    "value": "吉田 憲一郎（代表執行役 会長 CEO）\n十時 裕樹（代表執行役 社長 COO 兼 CFO）",
                },
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {"name": "売上高", "year": "2024", "value": "5兆7,923億円"},
                {"name": "売上高", "year": "2023", "value": None},
                {"name": "売上高", "year": "2022", "value": None},
                {"name": "従業員数", "year": "2024", "value": "約11万人"},
                {"name": "従業員数", "year": "2023", "value": None},
                {"name": "従業員数", "year": "2022", "value": None},
                {"name": "当期純利益", "year": "2024", "value": "4,177億円"},
                {"name": "当期純利益", "year": "2023", "value": None},
                {"name": "当期純利益", "year": "2022", "value": None},
                {"name": "資本金", "year": "2024", "value": None},
                {"name": "資本金", "year": "2023", "value": None},
                {"name": "資本金", "year": "2022", "value": None},
            ],
            "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ"},
                {"name": "代表者", "value": "十時裕樹"},
                {"name": "本社所在地", "value": None},
                {"name": "売上高", "year": "2024", "value": "13兆207億円"},
                {"name": "売上高", "year": "2023", "value": None},
                {"name": "売上高", "year": "2022", "value": None},
                {"name": "従業員数", "year": "2024", "value": None},
                {"name": "従業員数", "year": "2023", "value": None},
                {"name": "従業員数", "year": "2022", "value": None},
                {"name": "当期純利益", "year": "2024", "value": None},
                {"name": "当期純利益", "year": "2023", "value": None},
                {"name": "当期純利益", "year": "2022", "value": None},
                {"name": "資本金", "year": "2024", "value": None},
                {"name": "資本金", "year": "2023", "value": None},
                {"name": "資本金", "year": "2022", "value": None},
            ],
            "source": "https://www3.nhk.or.jp/news/html/20240514/k10014449021000.html",
            "corporate_number": None,
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {"name": "競合企業1", "value": "サムスン電子"},
                {"name": "競合企業2", "value": "オムニビジョン"},
                {"name": "競合企業3", "value": "パナソニック"},
            ],
            "source": "https://semi-journal.jp/career/company/sony.html",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {"name": "競合企業1", "value": "パナソニックホールディングス株式会社"},
                {"name": "競合企業2", "value": "日立製作所"},
                {"name": "競合企業3", "value": "三菱電機株式会社"},
            ],
            "source": "https://www.onecareer.jp/articles/1136",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {
                    "name": "会社名",
                    "value": "ソニーグループ株式会社 (Sony Group Corporation)",
                },
                {
                    "name": "代表者",
                    "value": "会長 CEO 吉田 憲一郎、社長 COO 兼 CFO 十時 裕樹",
                },
                {"name": "本社所在地", "value": "〒108-0075 東京都港区港南1-7-1"},
                {"name": "事業1", "value": "ゲーム＆ネットワークサービス"},
                {"name": "事業2", "value": "音楽"},
                {"name": "事業3", "value": "映画"},
            ],
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/data/",
            "corporate_number": None,
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニー株式会社"},
                {"name": "代表者", "value": "槙 公雄"},
                {"name": "本社所在地", "value": "〒108-0075 東京都港区港南1-7-1"},
                {
                    "name": "事業1",
                    "value": "エンタテインメント・テクノロジー&サービス（ホームエンタテインメント、パーソナルエンタテインメント、イメージングエンタテインメント、プロフェッショナルイメージングテクノロジー、レンズテクノロジー&システム、メディアソリューション、モバイルコミュニケーションズ、ライフサイエンス&テクノロジー、ソフトウェアサービス、スポーツエンタテインメント、セキュアテクノロジー&ソリューション、VPテクノロジー&サービス、ネットワークサービス、他）",
                },
                {"name": "事業2", "value": None},
                {"name": "事業3", "value": None},
            ],
            "source": "https://www.sony.co.jp/corporate/",
            "corporate_number": None,
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {
                    "name": "事業1",
                    "value": "ゲーム＆ネットワークサービス (PlayStationなど)",
                },
                {"name": "事業2", "value": "音楽 (Sony Music Entertainment)"},
                {"name": "事業3", "value": "映画 (Sony Pictures Entertainment)"},
            ],
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {
                    "name": "求める人材像",
                    "value": "ソニーグループは、クリエイティビティとテクノロジーの力で世界を感動で満たすことを目指しており、その実現には、多様な才能と個性を持つ人材が不可欠です。具体的には、変化への対応力、主体性、高い倫理観、グローバルな視点、そして何よりも強い好奇心と情熱を持つ人材を求めています。また、チームワークを重視し、他者と協力しながら目標達成を目指せる協調性も重要な要素です。それぞれの事業分野において求められる専門性ももちろん重要ですが、それ以上に、ソニーのPurpose（存在意義）に共感し、企業理念に沿って行動できる人材が求められています。",
                },
                {"name": "スキル1", "value": "変化への対応力"},
                {"name": "スキル2", "value": "主体性"},
                {"name": "スキル3", "value": "高い倫理観"},
            ],
            "source": "https://www.sony.com/ja/SonyInfo/Jobs/recruit/",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {
                    "name": "求める人材像",
                    "value": "ソニーグループは、創造性、好奇心、そして何事にも挑戦しようとする意欲を高く評価しています。変化に柔軟に対応し、グローバルな視点を持って仕事に取り組める人材を求めています。また、高い倫理観と責任感、チームワークを重視し、多様な文化やバックグラウンドを持つ人々と協力して仕事を進められる協調性も重要視しています。",
                },
                {"name": "スキル1", "value": "創造性と革新力"},
                {"name": "スキル2", "value": "問題解決能力"},
                {"name": "スキル3", "value": "コミュニケーション能力"},
            ],
            "source": "https://www.openwork.jp/company.php?m_id=a0910000000FrQT",
            "corporate_number": "5010401067252",
        },
        {
            "response": [
                {"name": "会社名", "value": "ソニーグループ株式会社"},
                {"name": "代表者", "value": "吉田憲一郎"},
                {"name": "本社所在地", "value": "東京都港区港南1-7-1"},
                {
                    "name": "求める人材像",
                    "value": "ソニーグループは、創造性、好奇心、多様性を尊重し、変化に柔軟に対応できる人材を求めています。具体的には、高い専門性と問題解決能力、チームワーク力、グローバルな視点、そしてソニーの企業理念である『感動を創造し、世界中の人々に届け続ける』という精神に共感し、それを実践できる人材を期待しています。",
                },
                {"name": "スキル1", "value": "高い専門性と問題解決能力"},
                {"name": "スキル2", "value": "チームワーク力"},
                {"name": "スキル3", "value": "グローバルな視点"},
            ],
            "source": "https://www.sony.com/ja/SonyInfo/Jobs/newgrads/",
            "corporate_number": "5010401067252",
        },
    ]
    processed_data = tidy_response(data)
    print(json.dumps(processed_data, indent=4, ensure_ascii=False))
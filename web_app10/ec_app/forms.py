from django import forms
from .models import Product

# 問 2-3-1 RegisterForm クラスを作成しましょう。引数には ModelForm を指定しましょう。

    # 問 2-3-2 Meta クラスを作成しましょう。

        # 問 2-3-2-1 model には Product テーブルを指定しましょう。

        # 問 2-3-2-2 fields には product_name、price、product_detail、category、img を指定しましょう。

        # 問 2-3-2-3 labels には下記を指定しましょう。

    # 問 2-3-3 init 関数を作成しましょう。

        # 問 2-3-3-1 super().__init__() として、*args と **kwargs を継承しましょう。

        # 問 2-3-3-2 self.label_suffix に '' を指定して、ラベル名の横にあるコロンを非表示にしましょう。

        # 問 2-3-3-3 for 文で self.fields.values() を回しましょう。

            # 問 2-3-3-4 それぞれの field の placeholder と class を変更しましょう。placeholder には field.label、class には form-control を指定しましょう。


# 問 4-4-1 SearchProductForm クラスを作成しましょう。引数には ModelForm を指定しましょう。

    # 問 4-4-2 Meta クラスを作成しましょう。

        # 問 4-4-3 model に Product、fields に category、labels に {'category':'カテゴリー'} を指定しましょう。

    # 問 4-4-4 init 関数を作成しましょう。

        # 問 4-4-5 super().__init__() として、*args と **kwargs を継承しましょう。

        # 問 4-4-6 self.label_suffix を 空で指定しましょう。

        # 問 4-4-7 self.fields.values() を field 変数として for 文で回しましょう。

            # 問 4-4-8 class に form-control を指定しましょう。

            # 問 4-4-9 field.required に False を指定しましょう。

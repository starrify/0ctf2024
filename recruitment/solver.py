import segno


def main():
    #payload = '{"name":"滌漾火珈豆谷欝寵齦棧","email":"ĄąŁęțÿżÀÁćæçöśű@POD-ASIA.RECRUITMENT.MARS.TECH","phone":"껪ㇴ㍂舘덃駱縷긭ㇼ蘭㍑糧곀뇂㍅㋗懲궒","languages":[3,3,3,3]}'
    segments = [
        ('{languages:[3,3,3,3],name:"', segno.consts.MODE_BYTE),
        ('滌漾火珈豆谷欝寵齦棧', segno.consts.MODE_KANJI),
        ('",email:"', segno.consts.MODE_BYTE),
        ('ĄąŁęțÿżÀÁćæçöśű@', segno.consts.MODE_BYTE, 'iso8859-16'),
        ('POD-ASIA.RECRUITMENT.MARS.TECH', segno.consts.MODE_ALPHANUMERIC),
        ('",phone:"', segno.consts.MODE_BYTE),
        ('껪ㇴ㍂舘덃駱縷긭ㇼ蘭㍑糧곀뇂㍅㋗懲궒"}', segno.consts.MODE_BYTE, 'utf-16-be'),
    ]
    qrcode = segno.make(segments, version=7, error="L", eci=True)
    qrcode.save("qrcode.png", scale=2)
    # XXX: afterwards manually edit the ec bits to make them look "high" -- the decoder won't complain


if __name__ == "__main__":
    main()

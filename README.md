# KHDL
## API Phong Vũ
### method: GET
### API: https://phongvu.vn/api/product/<product_id>
Cách lấy Product_ID:
VD: [Here](https://phongvu.vn/may-tinh-xach-tay-laptop-acer-spin-3-sp314-51-51le-nx-gzrsv-002-xam-s1810659.html?sku=1810659)
với python:
url = 'https://phongvu.vn/may-tinh-xach-tay-laptop-acer-spin-3-sp314-51-51le-nx-gzrsv-002-xam-s1810659.html?sku=1810659'
product_id = url.split('sku=')[-1]

==> API: https://phongvu.vn/api/product/1810659

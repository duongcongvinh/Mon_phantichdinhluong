import scrapy
from myAmazon.items import MyamazonItem
from scrapy.spidermiddlewares.httperror import HttpError


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]

    def start_requests(self): # gửi các yêu cầu HTTP đến các URL mà mình muốn cào dữ liệu
        # danh sách chứa các URL mà spider sẽ truy cập để cào dữ liệu
        urls=["https://www.amazon.com/s?k=men%27s+pants&i=fashion&rh=n%3A7141123011%2Cp_n_size_six_browse-vebin%3A2445352011%7C2445353011&dc&crid=B89G1XDQ6AC7&qid=1728462512&rnid=2445340011&sprefix=men%27s+%2Caps%2C540&ref=sr_nr_p_n_size_six_browse-vebin_13&ds=v1%3AYTLbhy2qLKM9qJx7YjbVdpPLssosODj4O74x2moZgd4"]
        # duyệt qua danh sách urls
        for url in urls: 
            # Đây là cách Scrapy tạo một yêu cầu HTTP (HTTP request) tới URL được chỉ định.
            yield scrapy.Request(   
                                    url=url, # URL được lấy từ vòng lặp for sẽ được sử dụng để gửi yêu cầu HTTP
                                    callback=self.parse, # Sau khi Scrapy nhận được phản hồi (response) từ URL, nó sẽ gọi hàm parse để xử lý dữ liệu trả về
                                    errback=self.errback_httpbin # Nếu có lỗi xảy ra trong quá trình gửi yêu cầu hoặc nhận phản hồi
                                )
    # xử lý nếu có lỗi
    def errback_httpbin(self, failure):
        self.logger.error(repr(failure)) 
        # self.logger.error(...): Dùng để ghi log (ghi lại thông tin) về lỗi với mức độ nghiêm trọng là "error"
        # Hàm repr chuyển đối tượng failure thành một chuỗi để có thể in ra log hoặc màn hình dễ hiểu hơn, mô tả chi tiết về lỗi đã xảy ra.

        # HttpError là một lớp lỗi trong Scrapy, được sử dụng để chỉ lỗi liên quan đến HTTP (khi yêu cầu HTTP trả về mã lỗi).
        if failure.check(HttpError): # kiểm tra xem lỗi có phải là lỗi HTTP (ví dụ lỗi phản hồi từ máy chủ với các mã trạng thái HTTP như 404, 500, 503...) hay không.
            response = failure.value.response # response chứa thông tin về phản hồi từ máy chủ mà gây ra lỗi.
            if response.status == 503:
                # Nếu mã trạng thái HTTP là 503 (Service Unavailable), ghi log lỗi này.
                self.logger.error("Received 503 response")
                # Thông báo rằng máy chủ đã trả về phản hồi 503 (dịch vụ không khả dụng).
    # xử lý phản hồi từ trang web
    def parse(self, response):
        productList = response.xpath("//div/div/div/span[@class='rush-component']/a/@href").getall() # xpath lấy link từng sản phẩm

        for productItem in productList: #Vòng lặp để duyệt từng link sp
            item = MyamazonItem() #tạo đối tượng lưu trữ thông tin sp
            item['productURL'] = response.urljoin(productItem)  # Lưu trữ URL đầy đủ của sản phẩm bằng cách kết hợp URL gốc và phần đường dẫn sản phẩm
            request = scrapy.Request(url = response.urljoin(productItem), callback = self.parseProductDetailPage)# Gửi một yêu cầu HTTP mới đến trang chi tiết của sản phẩm để lấy thông tin chi tiết
            request.meta['dataProduct'] = item  # Lưu trữ dữ liệu sản phẩm hiện tại vào meta của request để truyền đến hàm callback
            yield request #tiến hành cào web
        # Tìm URL của trang tiếp theo nếu có (phân trang)
        next_page = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href").get()
         # Nếu tìm thấy URL của trang tiếp theo, chuyển nó thành URL đầy đủ
        if next_page:
            next_page_url = response.urljoin(next_page)
            #self.logger.info(f"Next page URL: {next_page_url}")
            # Gửi yêu cầu HTTP đến trang tiếp theo để tiếp tục quá trình cào dữ liệu sản phẩm
        # self.logger.info(f"Next page URL: {next_page_url}") # Ghi log URL trang tiếp theo (tùy chọn)
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parseProductDetailPage(self, response):
        item = response.meta['dataProduct']
        # normalize-space(string(...)): Dùng để chuẩn hóa chuỗi bằng cách loại bỏ khoảng trắng thừa ở đầu và cuối
        # response.xpath(...): Sử dụng XPath để tìm và trích xuất
        # .get(): Lấy giá trị đầu tiên tìm thấy (trong trường hợp chỉ có một kết quả)
    
        item['productName'] = response.xpath("normalize-space(//*[@id='productTitle'])").get() # tên sản phẩm
        item['brand'] = response.xpath("normalize-space(//*[@id='brandInsights_feature_div_3']/div/div/h2)").get() # thương hiệu 
        item['price'] = response.xpath("normalize-space(//*[@id='corePrice_feature_div']/div/div/span[1]/span[1])").get() # giá 
        item['fabricType'] = response.xpath("normalize-space(//*[@id='productFactsDesktopExpander']/div[1]/div[1]/div/div[2]/span/span)").get() # loại vải
        item['closureType'] = response.xpath("normalize-space(//*[@id='productFactsDesktopExpander']/div[1]/div[4]/div/div[2]/span/span)").get() # loại khóa
        item['countryOfOrigin'] = response.xpath("normalize-space(//*[@id='productFactsDesktopExpander']/div[1]/div[5]/div/div[2]/span/span)").get() # xuất xứ sp
        item['customerssay'] = response.xpath("normalize-space(//*[@id='product-summary']/p[1])").get() # bình luận người dùng
        item['productDescription'] = response.xpath("normalize-space(//*[@id='productDescription']/p/span)").get() # mô tả chi tiết sản phẩm
        item['ratings'] = response.xpath("normalize-space(//*[@id='acrCustomerReviewText'])").get() # số lượt đánh giá
        item['rate'] = response.xpath("normalize-space(//*[@id='cm_cr_dp_d_rating_histogram']/div[2]/div/div[2]/div/span/span)").get() # tỷ lệ đánh giá  
        item['about'] = response.xpath("normalize-space(//*[@id='productFactsDesktopExpander']/div[1]/ul[1]/span/li/span)").get() # mô tả sản phẩm
        yield item
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
            response = failure.value.response
            if response.status == 503:
                self.logger.error("Received 503 response")

    # xử lý phản hồi từ trang web
    def parse(self, response):
        productList = response.xpath("//div/div/div/span[@class='rush-component']/a/@href").getall()

        for productItem in productList:
            item = MyamazonItem()
            item['productURL'] = response.urljoin(productItem)
            request = scrapy.Request(url = response.urljoin(productItem), callback = self.parseProductDetailPage)
            request.meta['dataProduct'] = item
            yield request

        next_page = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            #self.logger.info(f"Next page URL: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parseProductDetailPage(self, response):
        item = response.meta['dataProduct']
        # normalize-space(string(...)): Dùng để chuẩn hóa chuỗi bằng cách loại bỏ khoảng trắng thừa ở đầu và cuối
        # response.xpath(...): Sử dụng XPath để tìm và trích xuất
        # .get(): Lấy giá trị đầu tiên tìm thấy (trong trường hợp chỉ có một kết quả)
    
        item['productName'] = response.xpath("normalize-space(//*[@id='productTitle'])").get()
        item['brand'] = response.xpath("normalize-space(//*[@id='brandInsights_feature_div_3']/div/div/h2)").get()
        item['price'] = response.xpath("normalize-space(//*[@id='corePrice_feature_div']/div/div/span[1]/span[1])").get()
        item['fabricType'] = response.xpath("normalize-space(//*[@id='productFactsDesktopExpander']/div[1]/div[1]/div/div[2]/span/span)").get()
        item['closureType'] = response.xpath("normalize-space(//*[@id='productFactsDesktopExpander']/div[1]/div[4]/div/div[2]/span/span)").get()
        item['countryOfOrigin'] = response.xpath("normalize-space(//*[@id='productFactsDesktopExpander']/div[1]/div[5]/div/div[2]/span/span)").get()
        item['describe'] = response.xpath("normalize-space(//*[@id='productFactsDesktopExpander']/div[1]/ul[1]/span/li/span)").get()
        item['productDescription'] = response.xpath("normalize-space(//*[@id='productDescription']/p/span)").get()
        item['ratings'] = response.xpath("normalize-space(//*[@id='acrCustomerReviewText'])").get()
        item['rate'] = response.xpath("normalize-space(//*[@id='cm_cr_dp_d_rating_histogram']/div[2]/div/div[2]/div/span/span)").get()
        
        yield item
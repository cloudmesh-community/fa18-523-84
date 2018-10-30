## Wink :smiley: fa18-523-84


|          |                               |
| -------- | ----------------------------- |
| title    | Wink                          | 
| status   | 90                            |
| section  | Technologies To Be Integrated |
| keywords | Technologies To Be Integrated |


Apache Wink is a Java based framework which allows a user to develop and work with RESTful web services [01].  This tool was built by implementing the JAX-RS framework; the Java API which provides support for creating web services [02].  Wink provides both a client and server module.  The server module facilitates the development of REST services and the client module consumes these services [03]. The benefit that Apache Wink provides is that the framework makes it easier for the developer by separating out the low-level details and the business application [03].  This allows the developer to focus on the details and logic of the application being developed rather than spending time sorting through the technical aspects of REST web services.

Wink uses "building blocks" to contain particular REST components [03].  The service implementation building blocks consist of HTTP methods, URL query parameters, URL handling and URI dispatching to name a few [03].  The client building blocks contain resources such as client request, client response, input and output stream adapters.  Lastly, there is a collection of Wink runtime building blocks to deploy the process.

Apache Wink was moved to the Apache Attic in April 2017 [04].  This means that the project has reached its end-of-life and that it is no longer an active project with the Apache Software Foundation.  The Apache Attic is designed to be non-impactful to users meaning that applications developed using the existing Wink framework will still work.  However, the project will not have any future releases or bug fixes meaning that an application developer will want to explore other frameworks to develop RESTful web services.  Another Apache supported option to develop web services is Apache CXF.  This tool supports RESTful services and is actively being updated.  Some additional tool for developing RESTful web services are Spring MVC, Restlet and Jersey [05].


**Sources:**

  * 01 - Wink Site: https://svn.apache.org/repos/infra/websites/production/wink/content/index.html
  * 02 - Web Services: https://en.wikipedia.org/wiki/Java_API_for_RESTful_Web_Services
  * 03 - Wink Documentation: https://svn.apache.org/repos/infra/websites/production/wink/content/documentation/1.2.1/Apache_Wink_User_Guide.pdf
  * 04 - attic: http://attic.apache.org/projects/wink.html
  * 05 - other RESTful - https://dzone.com/articles/7-reasons-to-use-spring-mvc-for-developing-restful

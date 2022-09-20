using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace aws_1.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult addEmployee()
        {
            //ViewBag.Message = "Your application description page.";
          
            return View();
        }

        public ActionResult retrieveEmployee()
        {
       

            return View();
        }

        public ActionResult addSuccessful()
        {
 

            return View();
        }
        public ActionResult empOutput()
        {
            

            return View();
        }
    }
}
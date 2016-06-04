//
//  DetailViewController.swift
//  ECE158BFinal
//
//  Created by Max X on 5/6/16.
//  Copyright © 2016 Max Xing. All rights reserved.
//

import UIKit

class DetailViewController: UIViewController {

    var name: String!
    var x:Int = 1
    var myRootRef:Firebase!
    
    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!
    @IBOutlet weak var peopleNum: UILabel!
    @IBOutlet weak var locationName: UILabel!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        activityIndicator.startAnimating()
        
        print("it is "  + name)

        locationName.text = name
        
        myRootRef = Firebase(url:"https://ece158final.firebaseio.com/"+name+"/People")
        
        NSTimer.scheduledTimerWithTimeInterval(1.0, target: self, selector: ("updateLabel"), userInfo: nil, repeats: true);

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    func updateLabel(){
   
        myRootRef.observeEventType(.Value, withBlock: {
            snapshot in
            print("\(snapshot.key) -> \(snapshot.value)")
            self.peopleNum.text = (String) (snapshot.value)
            
        })
        
    
        activityIndicator.stopAnimating()

        let color = UIColor(red: CGFloat(self.x), green: 0, blue: 0, alpha: 1)
        
//        UIView.animateWithDuration(3, animations: {
//            self.view.backgroundColor = color
//        })
        
     }
    


    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}

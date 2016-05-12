//
//  LocationTableViewCell.swift
//  ECE158BFinal
//
//  Created by Max X on 5/6/16.
//  Copyright © 2016 Max Xing. All rights reserved.
//

import UIKit

class LocationTableViewCell: UITableViewCell {
    
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var ratingImageView: UIImageView!
    
    var locaiton: Location! {
        didSet {
            nameLabel.text = locaiton.name
        //    ratingImageView.image = imageForRating(locaiton.rating)
        }
    }
    
    func imageForRating(rating:Int) -> UIImage? {
        let imageName = "\(rating)Stars"
        return UIImage(named: imageName)
    }
    
    
}

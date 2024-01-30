import torch


def compute_iou(outputs, labels, num_classes):
    intersection = torch.zeros(num_classes)
    union = torch.zeros(num_classes)
    
    for i in range(num_classes):
        pred_mask = outputs == i
        label_mask = labels == i
        
        intersection[i] = torch.logical_and(pred_mask, label_mask).sum().item()
        union[i] = torch.logical_or(pred_mask, label_mask).sum().item()

    return intersection, union, intersection / union


def calculate_miou(outputs, labels, num_classes):
    intersection, union, iou = compute_iou(outputs, labels, num_classes)
    valid_classes = union != 0  # Exclude classes with no ground truth pixels
    
    # Compute mean IoU over valid classes
    mean_iou = torch.mean(iou[valid_classes])
    
    return mean_iou.item()


def calculate_exg_index(pixel):
    
    # The [:3] extracts the first three elements (RGB values)
    red, green, blue = pixel[:3]  
    # print(f"Red: {red}\n, Green: {green}\n, Blue: {blue}")

    index = 2 * green - red - blue
    # print(f"Index: {index}")
    return index
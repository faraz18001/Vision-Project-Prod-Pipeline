## Automate Anotation Tools

## Plans

| Plan | Cost | Credits/Month |
|------|------|---------------|
| Free | $0 | 1,000 |
| Starter | $49/mo | 10,000 |
| Core | $79/mo | 25,000+ |
| Enterprise | Custom | Unlimited |

## Your Project Cost

- **Dataset size:** ~6,700 images
- **Recommended:** Starter plan ($49/month) - covers full dataset in one month
- **Budget option:** Free tier over 7 months

## What Credits Cover

| Action | Credits Used |
|--------|--------------|
| 1 inference (auto-label) | 1 credit |
| 100 AI-labeled images | 100 credits |
| 30 min GPU training | ~1,000 credits |

## Overage

$0.003 per API call after credits exhausted.

## Comparison

| Method | Cost | Speed |
|--------|------|-------|

| Roboflow API | $49/mo | Fast (cloud) |

# SAM Pipeline on AWS

## Processing Time (~6,700 images)

| GPU Instance | Speed | Total Time |
|--------------|-------|------------|
| g4dn.xlarge (T4) | ~1-2 sec/image | 2-4 hours |
| g5.xlarge (A10G) | ~0.5-1 sec/image | 1-2 hours |
| p3.2xlarge (V100) | ~0.3 sec/image | 30-60 min |

## AWS Cost

| Instance | $/hour | For 4 hours |
|----------|--------|-------------|
| g4dn.xlarge | $0.53 | ~$2 |
| g5.xlarge | $1.01 | ~$4 |
| p3.2xlarge | $3.06 | ~$12 |
